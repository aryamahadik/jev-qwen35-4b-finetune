"""Tests for families/T12/freeze_v2.py (nothing is written to the pools; Haiku is never run).

  contract     validate_answer / read_answer_file: exact keys, qids from the task's chunk, each answered once, a texts list
               of exactly the asked length, a G-LEX meaning copied exactly; an invalid, missing or excluded (audit failed)
               file is rejected whole and never edited
  votes        record_votes follows the kit rule: 2 agreeing reads admit, one other pick rejects for good, one read is
               pending, precedence needs 3; g3h_results: exact match per note, an unanswered or wrong note is dropped
  lint         lint_redo2 on the real author answer equals build_redo2's own lint and the plan file on disk
  integration  one in-memory assemble() over the real files: v1 is reproduced and kept unchanged, targets are the v1
               targets, the verdict follows the gates, pending forms never enter the pool, provenance points at real
               files, the output is deterministic, no existing file changes, write goes to pools_v2 only and refuses a
               re-freeze or a blocked run, an excluded or invalid read leaves the forms pending and the verdict SHORT,
               and load_pools / make_ctx build real units that pass G2, G3, G4, G-SL, G-LEX and G-TW
Run (from lean/):
  PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -B -m pytest -q -p no:cacheprovider c2_build/families/T12/test_freeze_v2.py
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

from c2_kit import chunker as CH  # noqa: E402
from c2_kit import lexicon as L  # noqa: E402
from families.T12 import extract_build as EB  # noqa: E402
from families.T12 import freeze_v2 as FZ  # noqa: E402
from families.T12 import plugin as P  # noqa: E402
from families.T12 import pool_freeze as PF  # noqa: E402

T12 = Path(__file__).resolve().parent
MINE = {"freeze_v2.py", "test_freeze_v2.py"}


# ------------------------------------------------------------------------------------------------ helpers
def _bytes(obj) -> bytes:
    return json.dumps(obj).encode("utf-8")


def _items(n=3, **extra):
    return {f"q{i:010d}": {"qid": f"q{i:010d}", **extra} for i in range(n)}


# ------------------------------------------------------------------------------------------------ contract
def test_validate_answer_accepts_the_exact_contract():
    it = _items()
    ans, probs = FZ.validate_answer("author_skin", _bytes([{"qid": q, "texts": ["a", "b"]} for q in it]), it, 2)
    assert probs == [] and set(ans) == set(it) and all(set(a) == {"texts"} for a in ans.values())
    ans, probs = FZ.validate_answer("author_pack", _bytes([{"qid": q, "pack": {"org": "x"}} for q in it]), it)
    assert probs == []
    ans, probs = FZ.validate_answer("extract_g3h", _bytes([{"qid": q, "clerk": "Dana Okafor", "dept": "x"} for q in it]), it)
    assert probs == [] and ans[next(iter(it))] == {"clerk": "Dana Okafor", "dept": "x"}
    ans, probs = FZ.validate_answer("extract_g3h", _bytes([{"qid": q, "clerk": "", "dept": ""} for q in it]), it)
    assert probs == []                       # an empty string is a string (the extractor found nothing): a G3-H mismatch


@pytest.mark.parametrize("name,mutate", [
    ("not json", lambda it: b"[{"),
    ("bad utf-8", lambda it: b"\xff\xfe[]"),
    ("top level object", lambda it: _bytes({"a": 1})),
    ("entry not an object", lambda it: _bytes(["x"])),
    ("extra key", lambda it: _bytes([{"qid": q, "texts": ["a", "b"], "note": "b"} for q in it])),
    ("missing key", lambda it: _bytes([{"qid": q} for q in it])),
    ("wrong key", lambda it: _bytes([{"qid": q, "pack": "a"} for q in it])),
    ("unknown qid", lambda it: _bytes([{"qid": q, "texts": ["a", "b"]} for q in it] + [{"qid": "qZZZ", "texts": ["a", "b"]}])),
    ("duplicate qid", lambda it: _bytes([{"qid": q, "texts": ["a", "b"]} for q in list(it) + list(it)[:1]])),
    ("unanswered", lambda it: _bytes([{"qid": q, "texts": ["a", "b"]} for q in list(it)[:-1]])),
    ("texts not a list", lambda it: _bytes([{"qid": q, "texts": "a"} for q in it])),
    ("too few texts", lambda it: _bytes([{"qid": q, "texts": ["a"]} for q in it])),
    ("too many texts", lambda it: _bytes([{"qid": q, "texts": ["a", "b", "c"]} for q in it])),
    ("text not a string", lambda it: _bytes([{"qid": q, "texts": ["a", 3]} for q in it])),
    ("duplicate json key", lambda it: b'[{"qid": "q0000000000", "texts": ["a", "b"], "texts": ["c", "d"]}]'),
    ("empty list", lambda it: b"[]"),
])
def test_validate_answer_rejects_the_whole_file(name, mutate):
    it = _items()
    ans, probs = FZ.validate_answer("author_skin", mutate(it), it, 2)
    assert ans is None and probs, name


def test_validate_answer_lex_and_g3h_value_rules():
    it = {"qa": {"qid": "qa", "text": "t", "choices": ["m1", "m2"]}}
    assert FZ.validate_answer("extract_lex", _bytes([{"qid": "qa", "meaning": "m2"}]), it)[1] == []
    for bad in ("m3", "M1", "m1 ", None, 2, ["m1"]):
        ans, probs = FZ.validate_answer("extract_lex", _bytes([{"qid": "qa", "meaning": bad}]), it)
        assert ans is None and probs, bad
    g = {"qa": {"qid": "qa", "text": "t", "schema": []}}
    for bad in ({"clerk": 5, "dept": "a"}, {"clerk": "a", "dept": None}):
        ans, probs = FZ.validate_answer("extract_g3h", _bytes([{"qid": "qa", **bad}]), g)
        assert ans is None and probs
    assert FZ.validate_answer("nope", b"[]", {})[1]


def test_read_answer_file_statuses_and_no_edit(tmp_path):
    it = _items()
    good = [{"qid": q, "texts": ["a", "b"]} for q in it]
    ok = tmp_path / "ok.json"
    ok.write_bytes(_bytes(good))
    before = ok.read_bytes()
    ans, rec = FZ.read_answer_file("r", "author_skin", "T-1", ok, it, set(), 2)
    assert ans and rec["status"] == "valid" and rec["sha256"] == hashlib.sha256(before).hexdigest()
    assert rec["n_expected"] == rec["n_answered"] == 3
    ans, rec = FZ.read_answer_file("r", "author_skin", "T-1", tmp_path / "missing.json", it, set(), 2)
    assert ans is None and rec["status"] == "missing"
    bad = tmp_path / "bad.json"
    bad.write_bytes(b"not json")
    ans, rec = FZ.read_answer_file("r", "author_skin", "T-2", bad, it, set(), 2)
    assert ans is None and rec["status"] == "invalid" and rec["problems"]
    ans, rec = FZ.read_answer_file("r", "author_skin", "T-1", ok, it, {"T-1"}, 2)
    assert ans is None and rec["status"] == "excluded"
    ans, rec = FZ.read_answer_file("r", "author_skin", "T-1", ok, it, set(), 2, task_diff=["chunks/x.json"])
    assert ans is None and rec["status"] == "invalid" and "differs from the rebuilt task" in rec["problems"][0]
    assert ok.read_bytes() == before and bad.read_bytes() == b"not json"      # never edited


def test_files_differ_reports_changed_and_missing_files(tmp_path):
    (tmp_path / "a.txt").write_text("one", encoding="utf-8")
    assert FZ.files_differ(tmp_path, {"a.txt": "one"}) == []
    assert FZ.files_differ(tmp_path, {"a.txt": "two", "b.txt": "x"}) == ["a.txt", "b.txt"]
    assert FZ.files_differ(tmp_path, {"a.txt": "two"}, skip=("a.txt",)) == []


# ------------------------------------------------------------------------------------------------ G-LEX votes
def _toy_registry():
    reg = L.LexiconRegistry("T99")
    reg.declare("cmp.le", "comparator", "at most the bound")
    reg.declare("cmp.lt", "comparator", "less than the bound")
    reg.declare("prec.P1", "precedence", "the first failing check decides")
    reg.declare("prec.P2", "precedence", "the last failing check decides")
    reg.add("no more than {X}", "cmp.le", slots={"X": "cents"})
    reg.add("below {X}", "cmp.lt", slots={"X": "cents"})
    reg.add("The first failing check in the check order decides the action.", "prec.P1")
    reg.unit_test_all()
    return reg


def _read(reg, seed, pick):
    """One read: a batch of every form and the answers {task_id: {qid: {"meaning"}}} (pick: form id -> meaning)."""
    b = CH.make_batch("extract_lex", "T99", reg.lexicon_items(seed=seed), seed=seed, prompt="read the phrase")
    ans = {}
    for c in b.chunks:
        ans[c["task_id"]] = {it["qid"]: {"meaning": pick(b.key[it["qid"]], it)} for it in c["items"]}
    return b, ans


def _right(reg):
    return lambda fid, it: reg.sems[reg.forms[fid].sem_id].meaning


def test_glex_two_agreeing_reads_admit_and_one_dissent_rejects():
    reg = _toy_registry()
    fid_le = next(f for f, x in reg.forms.items() if x.sem_id == "cmp.le")
    wrong = {s.sem_id: s.meaning for s in reg.sems.values()}
    probs = []
    for r in (1, 2):
        b, ans = _read(reg, f"r{r}", _right(reg))
        FZ.record_votes(reg, b, ans, probs, f"r{r}")
    assert probs == [] and reg.status(fid_le) == "admitted"
    reg2 = _toy_registry()
    for r, pick in ((1, _right(reg2)), (2, lambda fid, it: wrong["cmp.lt"] if reg2.forms[fid].sem_id == "cmp.le"
                                        else reg2.sems[reg2.forms[fid].sem_id].meaning), (3, _right(reg2))):
        b, ans = _read(reg2, f"r{r}", pick)
        FZ.record_votes(reg2, b, ans, probs, f"r{r}")
    assert reg2.status(fid_le) == "rejected"                 # one other pick rejects for good, whatever the others say
    assert all(reg2.status(f) == "admitted" for f, x in reg2.forms.items() if x.sem_id != "cmp.le" and x.kind == "comparator")


def test_glex_one_read_is_pending_and_precedence_needs_three():
    reg = _toy_registry()
    probs = []
    b, ans = _read(reg, "r1", _right(reg))
    c = FZ.record_votes(reg, b, ans, probs, "r1")
    assert c["agrees"] == len(reg.forms) and all(reg.status(f) == "pending" for f in reg.forms)
    b, ans = _read(reg, "r2", _right(reg))
    FZ.record_votes(reg, b, ans, probs, "r2")
    prec = next(f for f, x in reg.forms.items() if x.kind == "precedence")
    assert reg.status(prec) == "pending"                     # 2/2 is not enough for precedence
    cmp_ids = [f for f, x in reg.forms.items() if x.kind == "comparator"]
    assert all(reg.status(f) == "admitted" for f in cmp_ids)
    b, ans = _read(reg, "r3", _right(reg))
    FZ.record_votes(reg, b, ans, probs, "r3")
    assert reg.status(prec) == "admitted" and probs == []


def test_glex_a_task_without_a_valid_answer_gives_no_vote_and_a_missing_qid_is_skipped():
    reg = _toy_registry()
    probs = []
    b, ans = _read(reg, "r1", _right(reg))
    c = FZ.record_votes(reg, b, {}, probs, "r1")             # the whole file was rejected
    assert c["task_without_valid_answer"] == len(b.chunks) and all(not f.extractions for f in reg.forms.values())
    tid = b.chunks[0]["task_id"]
    some = next(iter(ans[tid]))
    del ans[tid][some]
    FZ.record_votes(reg, b, ans, probs, "r1")
    voted = [f for f in reg.forms.values() if f.extractions]
    assert len(voted) == len(reg.forms) - 1 and probs == []
    FZ.record_votes(reg, b, ans, probs, "r1-again")          # the same extractor twice is refused, not counted
    assert probs and all(len(f.extractions) <= 1 for f in reg.forms.values())


# ------------------------------------------------------------------------------------------------ G3-H
def test_g3h_exact_match_unanswered_and_mismatch():
    fields = EB.g3h_fields()
    from c2_kit import g3h
    expected = {f"g3h|free|a|memo|{i}|0": {"clerk": "Dana Okafor", "dept": "facilities"} for i in range(3)}
    items = [(iid, g3h.extraction_item(f"Note from Dana Okafor, facilities team ({i}).", fields))
             for i, iid in enumerate(sorted(expected))]
    b = CH.make_batch("extract_g3h", "T12", items, seed="g3h-toy", prompt="extract")
    res = {"g3h": b, "g3h_expected": expected}
    tid = b.chunks[0]["task_id"]
    qs = [it["qid"] for it in b.chunks[0]["items"]]
    inv = {q: b.key[q] for q in qs}
    answers = {tid: {qs[0]: {"clerk": "Dana Okafor", "dept": "facilities"},
                     qs[1]: {"clerk": "", "dept": "facilities"}}}            # qs[2] unanswered
    rep, det = FZ.g3h_results(res, answers)
    assert det[inv[qs[0]]]["ok"] and not det[inv[qs[1]]]["ok"] and det[inv[qs[2]]]["diffs"] == ["unanswered"]
    assert sorted(rep["quarantined"]) == sorted([inv[qs[1]], inv[qs[2]]])
    rep, det = FZ.g3h_results(res, {})                                          # the file was rejected: all dropped
    assert not any(d["ok"] for d in det.values())


# ------------------------------------------------------------------------------------------------ lint
def test_lint_redo2_equals_build_redo2_and_the_plan_file():
    br = FZ._build_redo2()
    rb = br.author_batch()
    got, probs, sha = br.load_author(rb)
    assert probs == []
    mine = FZ.lint_redo2(br, rb, got, sha)
    theirs = br.run_lint()
    assert mine["kept"] == theirs["kept"] and mine["counts"] == theirs["counts"] and mine["pieces"] == theirs["pieces"]
    plan = json.loads((br.PLAN / "lint_r2.json").read_text(encoding="utf-8"))
    assert plan["kept"] == mine["kept"] and plan["answer_sha256"] == mine["answer_sha256"]
    assert mine["counts"] == {"cmp.le/kept": 12, "cmp.lt/kept": 12}


def test_redo_extract_files_equal_the_files_build_redo2_writes():
    br = FZ._build_redo2()
    lint = json.loads((br.PLAN / "lint_r2.json").read_text(encoding="utf-8"))
    files, _rows = br.extract_files(lint)
    mine = {}
    for _r, b in br.glex_batches(lint):
        mine.update(FZ.redo_extract_files(br, b))
    assert {k: v for k, v in files.items() if k not in ("TASKS.json", "answers/README.txt")} == mine


# ------------------------------------------------------------------------------------------------ integration
def _snapshot() -> dict:
    """sha256 of every existing file the freeze reads or could touch: T12 (except pools_v2 and this step's own files)
    and the kit."""
    out = {}
    for root in (T12, C2_BUILD / "c2_kit"):
        for p in sorted(root.rglob("*")):
            if not p.is_file() or "__pycache__" in p.parts or "pools_v2" in p.parts or p.name in MINE:
                continue
            out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


@pytest.fixture(scope="module")
def v1():
    return PF.build()


@pytest.fixture(scope="module")
def run_a(v1):
    before = _snapshot()
    a = FZ.assemble(v1=v1)
    return a, before


def test_v1_is_reproduced_and_nothing_existing_changed(run_a):
    a, before = run_a
    assert a["integrity"]["ok"], a["integrity"]["problems"]
    assert a["blockers"] == [], a["blockers"]
    assert _snapshot() == before                                  # no answer, plan, pool or code file was touched
    man = json.loads((FZ.POOLS_V1 / "manifest.json").read_text(encoding="utf-8"))
    assert man["version"] == "pool-freeze-v1" and a["integrity"]["manifest_sha256"] == FZ.sha_file(FZ.POOLS_V1 / "manifest.json")


def test_every_answer_file_on_disk_is_checked_and_valid(run_a):
    a, _ = run_a
    on_disk = sorted(p.name for d in (T12 / "haiku" / "author" / "answers", T12 / "haiku" / "extract" / "answers",
                                      T12 / "haiku" / "redo2" / "author" / "answers",
                                      T12 / "haiku" / "redo2" / "extract" / "answers") for p in d.glob("T12-*.json"))
    recs = a["records"]
    assert sorted(Path(r["file"]).name for r in recs) == on_disk and len(on_disk) == 45
    assert all(r["status"] == "valid" and not r["problems"] and r["n_answered"] == r["n_expected"] for r in recs)
    for r in recs:                                                 # the recorded sha is the file's own sha
        assert r["sha256"] == FZ.sha_file(C2_BUILD / r["file"])
    assert a["stray"] == [] and a["unknown_rounds"] == [] and a["excluded"] == []


def test_targets_are_the_v1_targets_and_the_verdict_follows_the_gates(run_a):
    a, _ = run_a
    assert FZ.targets_unchanged() == [] and FZ.G0_TARGETS is PF.G0_TARGETS
    man = json.loads((FZ.POOLS_V1 / "manifest.json").read_text(encoding="utf-8"))
    v1_rows = {(r["pool"], r["metric"]): r for r in man["shortfalls"]}
    for r in a["short_rows"]:
        v = v1_rows.get((r["pool"], r["metric"]))
        if v and v["target"] is not None:
            assert (r["target"], r["op"]) == (v["target"], v["op"])        # no target lowered
    met = [r for r in a["short_rows"] if r["met"] is not None]
    assert a["ready"] == (not a["blockers"] and all(r["met"] for r in met) and a["gates"]["G-LEX"]["pass"]
                          and a["gates"]["plugin"]["pass"] and a["gates"]["G3-H"]["kept_notes_all_pass"])
    assert a["short"] == [] and a["ready"]


def test_redo2_forms_are_admitted_on_two_reads_and_the_coverage_is_met(run_a):
    a, _ = run_a
    cmp_rows = a["items"]["comparators"]
    assert len(cmp_rows) == 21 + 24
    cover = next(r["value"] for r in a["short_rows"] if r["metric"].startswith("comparator forms cover"))
    assert all(v > 0 for v in cover.values()) and cover == {"cmp.le/count": 12, "cmp.le/cents": 10,
                                                           "cmp.lt/count": 13, "cmp.lt/cents": 10}
    reg = a["reg2"]
    for p in a["lint"]["kept"]:
        f = reg.forms[p["form_id"]]
        assert reg.status(p["form_id"]) == "admitted" and len({e for e, _ in f.extractions}) == 2
        assert all(s == f.sem_id for _, s in f.extractions)
    v1_count = next(fid for fid, f in reg.forms.items() if f.kind == "comparator" and dict(f.slots)["X"] == "count"
                    and f.haiku_task_id.startswith("T12-author_lexicon-358ef9ed"))
    assert len({e for e, _ in reg.forms[v1_count].extractions}) == 4        # 2 v1 reads + the 2 percent-bound re-reads
    assert reg.status(v1_count) == "admitted"


def test_pool_holds_only_admitted_forms_and_rejected_forms_stay_out(run_a):
    a, _ = run_a
    reg = a["reg2"]
    used = {r["form_id"] for pool in FZ.LEX_POOLS for r in a["items"][pool]}
    assert used and all(reg.status(f) == "admitted" for f in used)
    lex = a["lex_adm"]
    assert {f["form_id"] for f in lex["forms"]} == {fid for fid in reg.forms if reg.status(fid) == "admitted"} == used
    rejected = {fid for fid in reg.forms if reg.status(fid) == "rejected"}
    assert len(rejected) == 4 and rejected.isdisjoint(used)
    assert {q["form_id"] for q in a["quar"] if q["stage"] == "G-LEX"} == rejected
    assert a["gates"]["G-LEX"]["pass"] and a["gates"]["G-LEX"]["not_admitted"] == {}


def test_v1_pieces_carry_over_unchanged_and_counts_only_grow(run_a, v1):
    a, _ = run_a
    for stem in FZ.ITEM_POOLS:
        if stem == "comparators":
            assert a["items"][stem][:len(v1["items"][stem])] == v1["items"][stem]
        else:
            assert a["items"][stem] == v1["items"][stem]
    assert a["carry"]["comparators"] == {"v1_items_kept_unchanged_in_order": True, "v1_items_dropped_by_reread": [],
                                        "added": 24}
    assert [q for q in a["quar"]] == v1["quar"]                       # no new quarantine row: all 24 forms admitted
    texts = FZ.pool_file_texts(a["items"], a["lex_adm"], a["quar"])
    for name in ("packs.json", "skins.json", "attacks.json", "documents.json", "wordings.json", "precedence.json",
                 "quarantine.json"):
        assert texts[name] == (FZ.POOLS_V1 / name).read_text(encoding="utf-8"), name       # byte for byte
    assert texts["comparators.json"] != (FZ.POOLS_V1 / "comparators.json").read_text(encoding="utf-8")
    assert len(a["lex_adm"]["forms"]) == 268 + 24


def test_added_pieces_have_provenance_that_matches_the_answer_files(run_a):
    a, _ = run_a
    idx = json.loads((T12 / "haiku" / "redo2" / "REDO2_TASKS.json").read_text(encoding="utf-8"))["tasks"][0]
    man = json.loads(FZ.build_files(a)["MANIFEST.json"])
    added = man["redo2"]["added_forms"]
    assert len(added) == 24 and man["redo2"]["author_answer_sha256"] == FZ.sha_file(Path(idx["answer_file"]))
    for x in added:
        assert x["task_id"] == idx["task_id"] and x["prompt_sha"] == idx["prompt_sha"] and x["status"] == "admitted"
        assert len(x["reads"]) == 2 and {r[0] for r in x["reads"]} == {
            c["task_id"] for _r, b in a["redo_batches"] for c in b.chunks}
    rows = {r["form_id"]: r for r in a["items"]["comparators"]}
    for x in added:
        r = rows[x["form_id"]]
        assert (r["task_id"], r["prompt_sha"], r["bound"], r["status"]) == (
            idx["task_id"], idx["prompt_sha"], "count", "admitted")


def test_output_is_deterministic_and_the_manifest_hashes_match(run_a):
    a, _ = run_a
    f1 = FZ.build_files(a)
    f2 = FZ.build_files(a)
    assert f1 == f2
    man = json.loads(f1["MANIFEST.json"])
    assert man["ready"] is True and man["status"].startswith("READY") and man["shortfalls"] == []
    assert man["no_rows_generated"] and man["no_labels_set"] and man["targets_unchanged_vs_v1"]
    assert set(man["sha256"]) == set(f1) - {"MANIFEST.json"}
    for name, sha in man["sha256"].items():
        assert hashlib.sha256(f1[name].encode("utf-8")).hexdigest() == sha
    assert man["supersedes"]["version"] == "pool-freeze-v1" and man["v1_integrity"]["reproduced_by_rebuild"]
    assert set(f1) == {f"{s}.json" for s in FZ.ITEM_POOLS} | {"lexicon.json", "quarantine.json", "MANIFEST.json",
                                                             "VALIDATION_REPORT.json"}
    rep = json.loads(f1["VALIDATION_REPORT.json"])
    assert rep["files_total"] == 45 and rep["files_valid"] == 45 and rep["files_not_valid"] == []


def test_the_frozen_pools_v2_on_disk_equal_a_fresh_rebuild(run_a):
    """After `freeze` has run, pools_v2/ is exactly what the code produces again from the same inputs."""
    a, _ = run_a
    if not (FZ.POOLS_V2 / "MANIFEST.json").is_file():
        pytest.skip("pools_v2 not frozen yet")
    files = FZ.build_files(a)
    on_disk = {p.name: p.read_text(encoding="utf-8") for p in FZ.POOLS_V2.glob("*.json")}
    # One recorded statistic follows the CURRENT plugin, not the pool: the dry run's count of percent cards among 500
    # sampled specs (gates.plugin.percent_cards; 250 at the freeze, 243 since G0 v2.2 drew 8 cards per sampler). Every
    # pool file, the answer shas and every other manifest field must be byte for byte what was frozen.
    def without_dry_run_stat(text):
        obj = json.loads(text)
        obj["gates"]["plugin"].pop("percent_cards", None)
        return obj
    assert {k: v for k, v in on_disk.items() if k != "MANIFEST.json"} == \
        {k: v for k, v in files.items() if k != "MANIFEST.json"}
    assert without_dry_run_stat(on_disk["MANIFEST.json"]) == without_dry_run_stat(files["MANIFEST.json"])
    assert json.loads(on_disk["MANIFEST.json"])["gates"]["plugin"]["percent_cards"] == 250     # as frozen
    assert json.loads(on_disk["MANIFEST.json"])["ready"] is True


def test_plugin_checks_cover_all_percent_values_and_the_dry_run(run_a):
    a, _ = run_a
    pc = a["gates"]["plugin"]
    assert pc["pass"] and pc["specs"] == 500 and pc["contract_errors"] == {} and pc["round_trip_failures"] == []
    assert pc["count_forms_round_tripped"] == 25 and pc["percent_values"] == [1, 3, 5, 2, 4] and pc["percent_cards"] > 100


def test_freeze_writes_only_pools_v2_and_refuses_re_freeze_and_blocked_runs(run_a, tmp_path, monkeypatch):
    a, _ = run_a
    target = tmp_path / "pools_v2"
    written = {}
    monkeypatch.setattr(FZ, "POOLS_V2", target)
    monkeypatch.setattr(FZ, "assemble", lambda **kw: a)
    monkeypatch.setattr(FZ.paths, "write_files", lambda root, files, **kw: written.update(root=Path(root), files=files))
    out = FZ.run(write=True)
    assert written["root"] == target != FZ.POOLS_V1 and set(written["files"]) == set(out["files"])
    assert "MANIFEST.json" in written["files"] and out["ready"] is True and out["written"] is True
    written.clear()
    out = FZ.run(write=False)                                                  # check: nothing is written
    assert out["written"] is False and not written
    monkeypatch.setattr(FZ, "assemble", lambda **kw: dict(a, blockers=["x is wrong"]))
    with pytest.raises(SystemExit):
        FZ.run(write=True)
    assert not written
    target.mkdir()
    (target / "MANIFEST.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(FZ, "assemble", lambda **kw: pytest.fail("a re-freeze must stop before any work"))
    with pytest.raises(SystemExit):
        FZ.run(write=True)


def test_excluded_redo2_reads_leave_the_forms_pending_and_the_verdict_short(v1):
    br = FZ._build_redo2()
    lint = json.loads((br.PLAN / "lint_r2.json").read_text(encoding="utf-8"))
    r1, r2 = [b.chunks[0]["task_id"] for _r, b in br.glex_batches(lint)]
    for ex in ((r1, r2), (r2,)):
        a = FZ.assemble(exclude=ex, v1=v1)
        assert {r["task_id"] for r in a["records"] if r["status"] == "excluded"} == set(ex)
        assert not a["ready"] and a["blockers"] == []
        assert [s for s in a["short"] if s.startswith("comparators: comparator forms cover") and "'cmp.le/count': 0" in s]
        assert a["gates"]["G-LEX"]["pass"]                                   # a pending form is simply not in the pool
        pend = [fid for p in a["lint"]["kept"] for fid in [p["form_id"]] if a["reg2"].status(fid) == "pending"]
        assert len(pend) == 24 and all(a["reg2"].status(f) != "admitted" for f in pend)
        assert len(a["items"]["comparators"]) == 21                       # only the v1 forms are in the pool
        assert a["items"]["comparators"] == v1["items"]["comparators"]


def test_an_invalid_redo2_author_answer_gives_no_forms_and_an_invalid_v1_file_blocks(v1, monkeypatch):
    real = FZ.read_answer_file
    rtid = FZ._build_redo2().author_batch().chunks[0]["task_id"]

    def bad_redo_author(rnd, kind, task_id, *args, **kw):
        ans, rec = real(rnd, kind, task_id, *args, **kw)
        if task_id == rtid:
            return None, dict(rec, status="invalid", problems=["simulated"])
        return ans, rec
    monkeypatch.setattr(FZ, "read_answer_file", bad_redo_author)
    a = FZ.assemble(v1=v1)
    assert a["lint"] is None and not a["ready"] and a["blockers"] == []
    assert [s for s in a["short"] if s.startswith("comparators: comparator forms cover")
            and "'cmp.le/count': 0" in s]                                     # the exact shortfall is reported
    assert len(a["items"]["comparators"]) == 21 and all(r["status"] == "unused" for r in a["records"]
                                                        if r["round"] == "redo2" and r["kind"] == "extract_lex")
    v1_tid = v1["out"]["res"]["g3h"].chunks[0]["task_id"]

    def bad_v1(rnd, kind, task_id, *args, **kw):
        ans, rec = real(rnd, kind, task_id, *args, **kw)
        if task_id == v1_tid:
            return None, dict(rec, status="invalid", problems=["simulated"])
        return ans, rec
    monkeypatch.setattr(FZ, "read_answer_file", bad_v1)
    a = FZ.assemble(v1=v1)
    assert not a["ready"] and any("v1 extract answer" in b for b in a["blockers"])
    assert a["gates"]["G3-H"]["notes_ok"] < 96                                # the unread notes are dropped


def test_a_changed_v1_pool_or_a_lowered_target_is_caught(v1, monkeypatch):
    items = dict(v1["items"], packs=list(v1["items"]["packs"])[:-1])          # v1 rebuild no longer equals pools/
    bad = FZ.v1_integrity(dict(v1, items=items), v1["out"])
    assert not bad["ok"] and any("packs.json" in x for x in bad["problems"])
    lowered = tuple(dict(t, target=(t["target"] - 1 if t["pool"] == "packs" and t["metric"] == "kept packs"
                                    else t["target"])) for t in PF.G0_TARGETS)
    monkeypatch.setattr(FZ, "G0_TARGETS", lowered)
    assert FZ.targets_unchanged() and "kept packs" in FZ.targets_unchanged()[0]


def test_an_unrecognised_round_directory_is_a_blocker(v1, monkeypatch):
    monkeypatch.setattr(FZ, "KNOWN_ROUNDS", ())
    a = FZ.assemble(v1=v1)
    assert a["unknown_rounds"] == ["redo2"] and not a["ready"] and any("does not ingest" in b for b in a["blockers"])


def test_load_pools_and_make_ctx_build_real_units(run_a, tmp_path):
    """Load the freeze as the generator would and build real units (nothing is written to the pools): every unit passes
    G2, G3, G4, G-SL, G-LEX and G-TW, only admitted forms are ever offered, and the redo2 forms are rendered."""
    from c2_kit import pipeline
    a, _ = run_a
    for name, text in FZ.build_files(a).items():
        (tmp_path / name).write_text(text, encoding="utf-8")
    pools = FZ.load_pools(tmp_path)
    ctx = FZ.make_ctx(pools)
    assert len(pools["skins"]) == 452 and len(pools["documents"]) == 96 and len(pools["attacks"]) == 39
    assert len(pools["packs"]) == 46 and len(pools["wordings"]) == 217 and len(pools["comparators"]) == 45
    ids = list(ctx.skins)
    assert len(ids) == len(set(ids)) == 452 + 96 + 39 + 217
    reg = ctx.lexicon
    assert all(reg.status(f) == "admitted" for f in reg.forms) and len(reg.forms) == 268 + 24
    assert all(reg.status(s.lexicon_ids[0]) == "admitted" for s in ctx.skins.values() if s.kind == "wording")
    redo_ids = {x["form_id"] for x in pools["comparators"] if x["task_id"].startswith("T12-author_lexicon-deaaa5ce")}
    used, bad = set(), []
    with FZ.packs_installed(pools):
        assert P.PACKS == tuple(pools["packs"])
        plugin = P.T12Plugin(lexicon=reg)
        for seed in range(6):
            for smp in plugin.SAMPLERS:
                sp = plugin.sample(seed, smp)
                if sp.structure.get("tol_kind") == "pct":
                    used.add(sp.slots["TOL_CMP"].value[1])
                r = pipeline.build_unit(plugin, sp, ctx, run_g15=False)
                if not r.ok:
                    bad.append((seed, smp, r.problems[:2]))
    assert P.PACKS != tuple(pools["packs"])                                  # restored after the block
    assert bad == []
    assert used & redo_ids                                                    # redo2 forms were drawn and rendered
