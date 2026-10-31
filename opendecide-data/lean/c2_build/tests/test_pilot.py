"""Tests for pilot.py, pilot_loaders.py and pilot_t37b.py (C2_DATA_SPEC 6.4 step 5). In memory only: the end-to-end
test runs the kit's reference family R00 through run_family(write=False), so nothing is written. Run from lean/:
  ../.venv/bin/python -m pytest -q c2_build/tests/test_pilot.py
"""
from __future__ import annotations

import contextlib
import json
import random
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
import pilot as P  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from c2_kit import chunker, g3h, g5h  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit.reference import r00, r00_fixtures  # noqa: E402

READY = ("T35", "T30", "T24", "T33", "T29", "T31", "T32", "T23", "T15", "T12", "T25", "T36", "T21", "T20")


# ------------------------------------------------------------------------------------------------ R00 as a pilot family

@contextlib.contextmanager
def _r00_kit():
    ctx = r00_fixtures.ctx()
    yield PL.FamilyKit("R00", C2B / "c2_kit" / "reference", r00.R00(lexicon=ctx.lexicon), ctx, "fixture", "none")


@pytest.fixture(scope="module")
def built():
    with _r00_kit() as kit:
        return kit, P.build_pilot(kit, 120, run_g15=False)


@pytest.fixture(scope="module")
def report(monkeypatch_module):
    monkeypatch_module.setitem(PL.LOADERS, "R00", _r00_kit)
    return P.run_family("R00", 120, write=False, run_g15=False, log=lambda m: None)


@pytest.fixture(scope="module")
def monkeypatch_module():
    mp = pytest.MonkeyPatch()
    yield mp
    mp.undo()


# ------------------------------------------------------------------------------------------------ loaders

def test_every_ready_family_has_a_loader_and_its_folder():
    assert set(READY) <= set(PL.LOADERS)
    assert PL.family_dir("T36") == C2B / "transfer" / "T36"
    assert PL.family_dir("t37b") == C2B / "t37b"
    assert PL.family_dir("T35") == C2B / "families" / "T35"
    for f in READY:
        assert PL.family_dir(f).is_dir(), f


def test_unknown_family_refused():
    with pytest.raises(PL.LoaderError):
        PL.open_family("T99")


def test_safe_read_refuses_never_open_paths():
    with pytest.raises(PermissionError):
        PL.safe_read(PL.HERE.parent / "ohs4_sealed" / "MANIFEST.json")
    with pytest.raises(PermissionError):
        PL.safe_read(Path("/private/tmp/claude-501/x.json"))


def test_check_shas_refuses_a_changed_file(tmp_path):
    p = tmp_path / "a.json"
    p.write_text("{}")
    PL.check_shas(tmp_path, {"a.json": PL.sha_file(p)}, ["a.json"])
    with pytest.raises(PL.LoaderError):
        PL.check_shas(tmp_path, {"a.json": "0" * 64}, ["a.json"])
    with pytest.raises(PL.LoaderError):
        PL.check_shas(tmp_path, {}, ["a.json"])


@pytest.mark.parametrize("fid", ["T20", "T21"])
def test_real_loader_builds_passing_units(fid):
    """Two quick real loaders (frozen pools, read only): a few units pass every program gate."""
    from c2_kit import pipeline
    with PL.open_family(fid) as kit:
        pl = kit.plugin
        train = [s for s in pl.SAMPLERS if s not in pl.HELD_OUT_SAMPLERS]
        ok = sum(pipeline.build_unit(pl, pl.sample(P.SEED_BASE + i, train[i % len(train)]), kit.ctx,
                                     run_g15=False).ok for i in range(8))
        assert ok >= 6


# ------------------------------------------------------------------------------------------------ build

def test_build_reaches_target_with_whole_units(built):
    kit, b = built
    st = b.stats
    assert st["rows_written"] >= 120 and st["reached_target"]
    assert len(b.infos) == st["rows_written"] == sum(len(u.rows) for u in b.units)
    assert set(st["training_samplers"]) == {"S1", "S2", "S3", "S4"}
    assert all(i.row["meta"]["sampler"] != "S5" for i in b.infos)
    ids = {i.row["id"] for i in b.infos}
    assert len(ids) == len(b.infos)
    assert all(x["a"] in ids and x["b"] in ids for x in b.rels)
    assert all(not R.validate_row(i.row) for i in b.infos)


def test_seeds_are_consecutive_per_sampler(built):
    _kit, b = built
    seeds = {}
    for i in b.infos:
        if i.row["role"] == "base":
            seeds.setdefault(i.row["meta"]["sampler"], set()).add(i.row["meta"]["seed"])
    assert set(seeds) == {"S1", "S2", "S3", "S4"}
    for s, v in seeds.items():
        assert P.SEED_BASE <= min(v) <= P.SEED_BASE + 3
        assert max(v) - min(v) < len(v) + 10                         # consecutive draws, few dropped


def test_row_info_matches_its_rendered_row(built):
    _kit, b = built
    for i in b.infos:
        assert i.rr.row is i.row
        assert i.spec.qform == i.row["meta"]["qform"]
        if i.rr.wording_id:
            fld, a, z = i.rr.regions[i.rr.wording_id]
            assert i.question == i.row[fld][a:z]
            assert i.question not in i.context or i.question in (i.row["state"] or "")


def test_recorder_is_removed_after_build(built):
    kit, _b = built
    assert "render" not in kit.plugin.__dict__


def test_program_gate_verdicts():
    b = P.Build("X", stats={"units_attempted": 10, "drops_by_gate": {"G2": 1, "G-SL": 2, "render": 1},
                            "drop_examples": {"G2": ["e"]}, "g4_metamorphic_checked": {"a": 1, "b": 1, "c": 1},
                            "per_sampler": {"S1": {"rows": 5}}})
    g = P.program_gates(b)
    assert g["G2"]["verdict"] == "fail" and g["G2"]["units_failed"] == 1
    assert g["G-SL"]["verdict"] == "pass" and g["G-SL"]["units_failed"] == 2
    assert g["G3"]["verdict"] == "pass"
    assert g["G4"]["verdict"] == "pass"
    assert g["drops_outside_gates"]["counts"] == {"render": 1}
    b.stats["g4_metamorphic_checked"] = {"a": 1}
    assert P.program_gates(b)["G4"]["verdict"] == "fail"


# ------------------------------------------------------------------------------------------------ G6 / G7 / G10

def _info(i, gold, *, card, q="Is it so?", ctx="text", wording="w0", qform="yn"):
    row = {"id": f"r{i}", "qtype": "noul", "gold": gold, "options": None, "state": ctx, "instructions": q,
           "card": None, "role": "base", "call_id": f"c{i}",
           "meta": {"card_id": f"k{card}", "sampler": f"S{i % 4 + 1}", "domain_pack": f"p{card}",
                    "wording_id": wording, "qform": qform, "format_style": "memo/text", "defs_style": "x",
                    "depth": 0, "deep": False, "difficulty_bin": None, "twin_kind": None,
                    "c2": {"skin_id": f"s{i % 7}", "register": "memo", "author_mode": "T"}}}
    return P.RowInfo(row, None, None, i, q, ctx, None)


def _balanced(n=400, seed=0):
    rnd = random.Random(seed)
    return [_info(i, int(rnd.random() < 0.5), card=i % 20, ctx=f"case {rnd.randrange(10 ** 6)} noted") for i in
            range(n)]


def test_g6_passes_on_label_free_text_and_fails_on_a_leaky_question():
    clean = P.g6(_balanced())
    assert clean["yes_no"]["n"] == 400
    leak = [_info(i, i % 2, card=i % 20, q="Is it fine?" if i % 2 else "Is it broken?", ctx=f"case {i}")
            for i in range(400)]
    res = P.g6(leak)
    assert res["verdict"] == "fail"
    assert any(f["view"] == "a_question" for f in res["fails"])


def test_g7_flags_a_planted_token():
    rows = _balanced(600, seed=3)
    assert P.g7(rows)["verdict"] == "pass"
    planted = [_info(i, i % 2, card=i % 20, ctx=("urgent " if i % 2 else "") + f"case {i}") for i in range(600)]
    res = P.g7(planted)
    assert res["verdict"] == "fail"
    assert any(o["feature"] == "urgent" for o in res["yes_no_raw_fails"])


class _Stub:
    FAMILY = "R00"
    TIER = "everyday"
    QFORMS = {}


def test_g10_yes_rate_band():
    ok = [_info(i, i % 2, card=i % 20, q="Is it so?" if i % 10 else "Is it not so?") for i in range(400)]
    res = P.g10(ok, [], _Stub())
    assert res["checks"]["yes_rate"]["verdict"] == "pass"
    skew = [_info(i, int(i % 10 < 6), card=i % 20) for i in range(400)]
    assert P.g10(skew, [], _Stub())["checks"]["yes_rate"]["verdict"] == "fail"


def test_g10_negation_shares():
    rows = [_info(i, i % 2, card=i % 20, q="Is it not the case that it is not so?" if i % 20 == 0 else
                  ("Is it not so?" if i % 5 == 0 else "Is it so?")) for i in range(400)]
    c = P.g10(rows, [], _Stub())["checks"]
    assert c["syntactic_negation_share"]["value"] >= 0.2
    assert c["double_negation_share"]["verdict"] == "pass"


# ------------------------------------------------------------------------------------------------ chunks

def test_g5h_chunks_two_independent_gold_free_reads(built):
    kit, b = built
    files, tasks, key = P.g5h_chunks(b.infos, "R00", kit.dir / "pilot")
    n = min(P.G5H_N, len(b.infos))
    assert key["n_rows"] == n and len(set(key["row_ids"])) == n
    a, bb = key["readers"]["A"], key["readers"]["B"]
    assert set(a["key"].values()) == set(bb["key"].values()) == set(key["row_ids"])
    assert not set(a["key"]) & set(bb["key"])                       # opaque ids differ between the reads
    assert {t["reader"] for t in tasks} == {"A", "B"}
    gold_of = {i.row["id"]: i.row["gold"] for i in b.infos}
    for t in tasks:
        text = files[str(Path(t["task_file"]).relative_to(kit.dir / "pilot"))]
        assert t["answer_file"] in text and "## Answer contract" in text and "## Items" in text
        items = json.loads(text.split("## Items (JSON; answer every item exactly once, keyed by its qid)\n\n", 1)[1])
        assert len(items) == t["n_items"] <= chunker.MAX_ITEMS
        for it in items:
            assert set(it) <= {"qid", "kind", "text", "question", "options", "definitions"}
            assert re.fullmatch(r"q[0-9a-f]{10}", it["qid"])
        for rid in key["row_ids"]:
            assert rid not in text
        assert Path(t["answer_file"]).parent.name == "answers" and "g5h" in t["answer_file"]
    assert all(str(gold_of[r]) for r in key["row_ids"])


def test_g3h_chunks_cover_mode_f_rows_and_keep_expected_facts_out(built):
    kit, b = built
    ff = [i for i in b.infos if i.row["meta"]["c2"]["author_mode"] == "F"]
    files, tasks, key = P.g3h_chunks(b.infos, kit.plugin, "R00", kit.dir / "pilot")
    if not ff:
        assert key is None and not tasks
        return
    assert key["n_rows"] + len(key["mode_f_rows_without_region"]) == len(ff)
    for rid, e in key["rows"].items():
        fields = [P.field_from_json(f) for f in e["fields"]]
        info = next(i for i in ff if i.row["id"] == rid)
        assert [f.name for f in fields] == [f.name for f in kit.plugin.extract_fields(info.spec)]
        assert set(e["expected"]) == {f.name for f in fields}
        assert e["template"] == info.row["meta"]["c2"]["skin_id"]
    for t in tasks:
        text = files[str(Path(t["task_file"]).relative_to(kit.dir / "pilot"))]
        assert '"expected"' not in text and t["answer_file"] in text
        items = json.loads(text.split("## Items (JSON; answer every item exactly once, keyed by its qid)\n\n", 1)[1])
        assert all(set(it) == {"qid", "text", "schema"} for it in items)


def test_field_json_round_trip():
    f = g3h.Field("category", "category", "what", (("surfaces", (("a", ("A", "Ay")), ("b", ("B",)))),))
    assert P.field_from_json(json.loads(json.dumps(P._field_json(f)))) == f


# ------------------------------------------------------------------------------------------------ end to end

def test_run_family_in_memory(report):
    g = report["gates"]
    for k in ("G2", "G3", "G4", "G-SL", "G-LEX", "G-TW", "G15", "G6", "G7", "G10", "overlay", "spec_3_0", "G3-H",
              "G5-H"):
        assert k in g, k
    assert g["G5-H"]["verdict"] == "pending" and g["G5-H"]["readers"] == 2
    assert report["files"]["n_rows"] >= 120 and report["written"] is False
    assert report["summary"]["verdict"] in ("PASS (pending Haiku gates)", "FAIL")
    assert len(report["gate_lines"]) >= 10
    assert all(t["answer_file"].endswith(".json") for ts in report["chunks"].values() for t in ts)


def test_score_helpers_rebuild_the_answer_key(built):
    kit, b = built
    files, tasks, key = P.g5h_chunks(b.infos, "R00", kit.dir / "pilot")
    a = key["readers"]["A"]
    raw = {}
    for qid, tid in a["task_of"].items():
        raw.setdefault(tid, []).append({"qid": qid, "answer": "yes", "confidence": 0.9})
    got, probs = chunker.load_answers(P._KeyBatch(a), raw)
    assert set(got) == set(key["row_ids"]) and not probs
    rows = [i.row for i in b.infos if i.row["id"] in set(key["row_ids"])]
    res = g5h.score(rows, key["items"], got, got, seed="t")
    assert res["n_read"] == len(rows)
