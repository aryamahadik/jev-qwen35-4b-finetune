"""Tests for the A61 (e) DI leak-check targets: di_g13.py and its wiring in g13_c2.py (draft ruling c2_build/zed_orch/di_train/A61_DRAFT.md).
Synthetic data only (pytest tmp_path); no DI file is read, listed or stat-ed (the quarantine paths are only compared as strings), no G13 run
over real data, no network. Run from lean/:
  ../.venv/bin/python -B -m pytest -q c2_build/tests/test_g13_c2_di.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import c2io  # noqa: E402
import di_g13 as D  # noqa: E402
import g13_c2 as G  # noqa: E402
from test_g13_c2 import A38, EVAL_SENT, _run, exports, fake_tools, row, world  # noqa: E402,F401  (fixtures of the end-to-end world)

g = G.g
A61_WITH_TAG = "> **Ruling A61 (17 Oct 2026): the DI-train block.**\n> - the HLE gap is accepted under tag A61-HLE.\n\nnext\n"
A61_NO_TAG = "> **Ruling A61 (17 Oct 2026): the DI-train block.**\n> - nothing about HLE.\n\nnext\n"

DI_WORDING = "Decide whether the claim is fully supported by the passages that follow and answer yes or no"
GSM_Q = "Mina buys seven crates of pears and each crate holds twelve pears so how many pears does she have in all"
HOVER_CLAIM = "The author of the novel set in the walled city was born in the same year as the founder of the old canal company"
TWEET = "oh great another monday what a delightful surprise for everybody on the train this morning"
DI_STATE = "Ravi owes Ines 45 coins after the autumn fair closes in the valley town."
DI_OPTIONS = ["Ravi", "Ines"]


def sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def pins_for(files: dict, complete=True, gaps=(D.HLE_GAP,), src_complete=True) -> dict:
    """A pin record with a fake sha256 per file. files = {target: [paths]}."""
    out = {"kit": {"repo": "https://github.com/apolinario/decision-index", "commit": "c" * 40, "edition": "release-v3"}}
    for t, ps in files.items():
        out[t] = {"complete": complete if t == "di03_public" else src_complete,
                  "gaps": list(gaps) if t == "di03_public" else [],
                  "files": {p: {"sha256": sha(p)} for p in ps}}
    return out


REAL_FILES = {t: list(D.FILES[t]) for t in D.TARGETS}


def make_di_exports(root: Path, pins: dict) -> Path:
    """The hashed exports exactly as g13_di/di_register.py export writes them (MANIFEST.json, wording8_u64.npy, structure_g13.json,
    record_ids.json), derived from the pinned files."""
    root.mkdir(parents=True, exist_ok=True)
    w8 = np.array(sorted(set(D.gram_u64(D.words(DI_WORDING)))), np.uint64)
    np.save(root / "wording8_u64.npy", w8)
    struct = [g.struct_g13(DI_STATE, DI_OPTIONS)]
    (root / "structure_g13.json").write_text(json.dumps(sorted(struct)))
    ids = {"gsm8k_question_sha256": [D.sha_hex(D.norm(GSM_Q))], "hover_claim_sha256": [D.sha_hex(D.norm(HOVER_CLAIM))],
           "hover_uid": ["uid-hover-1"], "hover_group": ["hpqa-77"], "isarcasm_text_sha256": [D.sha_hex(D.norm(TWEET))]}
    (root / "record_ids.json").write_text(json.dumps(ids))
    man = {"files": {n: {"sha256": g.sha256_file(root / n)} for n in D.DiExports.FILES}, "derived_from": D.pinned_files(pins),
           "counts": {"wording8": len(w8), "structure_g13": len(struct), **{k: len(v) for k, v in ids.items()}}}
    (root / "MANIFEST.json").write_text(json.dumps(man))
    return root


# ---- registration ---------------------------------------------------------------------------------------------------------
def test_the_di_files_are_on_the_engines_allow_list_and_di_test_stays():
    assert g.QUARANTINE_OK[0].endswith("ejs5_rows.jsonl") and "release-v1-rebuilt/selected-rows.jsonl" in g.QUARANTINE_OK[1]   # di_test as it was
    assert all(p in g.QUARANTINE_OK for p in D.QUARANTINE_OK) and len(set(g.QUARANTINE_OK)) == len(g.QUARANTINE_OK)
    for p in D.QUARANTINE_OK:
        assert g.allowed(g.REPO / p), p                                            # string logic only: nothing is opened
    other = "bench/external_quarantine/decision_index_03/work/artifacts/benchmark-suite/release-v2-rebuilt/other.jsonl"
    assert not g.allowed(g.REPO / other) and not g.allowed(g.REPO / "bench/external_quarantine/decision_index/repo/hub/manifest.json")
    D.patch_engine()
    D.patch_engine()
    assert list(g.QUARANTINE_OK).count(D.DI03_FILES[0]) == 1                        # idempotent


def test_the_c2_tools_never_open_the_di_files_and_their_names_are_not_greppable_as_training_data():
    for p in D.QUARANTINE_OK:
        assert c2io.refusal(g.REPO / p), p                                         # bench/external_quarantine/ is on the never-open list
        parts = [x.lower() for x in Path(p).parts]
        assert not any("ohs" in x or "jev" in x for x in parts) and "data" not in parts[:1]     # outside data/, no OHS / Jev name
        assert not any(x in ("runs", "results", "_work", "preds") for x in parts)              # the engine's NEVER pattern
    assert D.QROOT.startswith("bench/external_quarantine/") and D.QROOT.endswith("decision_index_03")


def test_engine_targets_are_unchanged_by_default_and_gain_exactly_the_two_di_targets(tmp_path, monkeypatch):
    monkeypatch.setattr(D, "PINS", tmp_path / "no_pins_yet.json")                    # independent of what g13_di/di_pins.json says today
    old = {t["name"] for t in g.targets()}
    assert "di_test" in old and not set(D.TARGETS) & old
    for run in ("seed", "candidates", "carry", "final"):
        base = {t["name"] for t in G.engine_targets(run)}
        assert not set(D.TARGETS) & base, run
        assert {t["name"] for t in G.engine_targets(run, True)} == base | set(D.TARGETS)
    tg = {t["name"]: t for t in G.engine_targets("candidates", True) if t["name"] in D.TARGETS}
    for n, t in tg.items():
        assert t["blind"] is True and t["kind"] == "generic" and t["status"] is None and t["methods"] == "all"
        assert t["paths"] == ["repo:" + p for p in D.FILES[n]] and t["note"] == D.NOTES[n]
    assert tg["di03_public"]["fields"] == ("state", "questions") and tg["di_src_splits"]["fields"] is None
    assert tg["di03_public"]["gap"] and tg["di_src_splits"]["gap"]                  # nothing is pinned yet: both are incomplete


def test_a_di_block_is_run_by_name_not_by_default(tmp_path, monkeypatch):
    assert G.default_blocks("candidates") == [b for b in c2io.ALL_TARGETS if b not in c2io.CARRY and b not in c2io.DI_BLOCKS]
    fam = tmp_path / "families"
    for n in ("ok_fam", "DI-KR"):
        (fam / n / "pools").mkdir(parents=True)
    monkeypatch.setattr(G, "HERE", tmp_path)
    monkeypatch.setattr(G, "FAMILY_DIRS", {})
    assert G.default_blocks("seed") == ["ok_fam"]


# ---- readiness and the HLE gap -------------------------------------------------------------------------------------------
def test_gap_for_needs_a_complete_pin_and_accepts_the_hle_gap_only_under_the_tag():
    assert "not built or fetched yet" in D.gap_for("di03_public", {}, A61_WITH_TAG)
    p = pins_for(REAL_FILES)
    assert D.gap_for("di_src_splits", p, A61_NO_TAG) is None                         # no HLE gap there
    assert "HLE not scanned (gated)" in D.gap_for("di03_public", p, A61_NO_TAG)
    assert "A61-HLE" in D.gap_for("di03_public", p, A38)                             # no A61 block at all
    assert D.gap_for("di03_public", p, A61_WITH_TAG) is None and D.complete(p, A61_WITH_TAG)
    assert not D.complete(p, A61_NO_TAG)
    other = pins_for(REAL_FILES, gaps=(D.HLE_GAP, "BRIGHT: 3 queries not rebuilt"))
    assert "BRIGHT" in D.gap_for("di03_public", other, A61_WITH_TAG)                  # any other gap makes the target incomplete
    assert D.gap_for("di03_public", pins_for(REAL_FILES, complete=False), A61_WITH_TAG)
    assert D.gap_for("di_src_splits", pins_for(REAL_FILES, src_complete=False), A61_WITH_TAG)
    assert D.hle_accepted(A61_WITH_TAG) and not D.hle_accepted(A61_NO_TAG) and not D.hle_accepted("")
    assert "A61-HLE" not in D.a61_block("x\n> **Ruling A60 (x)**\n> A61-HLE in the wrong block\n")


def test_needs_di_follows_the_run_the_blocks_and_the_pins():
    units_di = [{"rows_src": [{"meta": {"family": "DI-KR"}}]}]
    units_core = [{"rows_src": [{"meta": {"family": "T28"}}]}]
    cand = lambda b, u=(): {"c2_cand_" + b: {"block": b, "units": list(u)}}   # noqa: E731
    none, ok = {}, pins_for(REAL_FILES)
    assert D.needs_di("candidates", cand("DI-TS"), none) and D.needs_di("seed", {"c2_seed_DI-LANG": {"block": "DI-LANG", "units": []}}, none)
    assert not D.needs_di("candidates", cand("T28", units_core), ok, A61_WITH_TAG)   # a core block's candidates run: as before
    assert not D.needs_di("carry", cand("F5"), ok, A61_WITH_TAG)
    final = lambda u: {"c2_final": {"block": "final", "units": u}}                    # noqa: E731
    assert not D.needs_di("final", final(units_core), none)                           # A61 e 6: no DI target ready, no DI row: core only
    assert D.needs_di("final", final(units_core), ok, A61_WITH_TAG)                  # ready: every block meets them
    assert not D.needs_di("final", final(units_core), ok, A61_NO_TAG)                # the HLE gap is not accepted yet: not complete
    assert D.needs_di("final", final(units_di), none)                                 # DI rows in the mix: the targets must be there


# ---- exports, the program methods ------------------------------------------------------------------------------------
@pytest.fixture()
def di_world(tmp_path):
    pins = pins_for(REAL_FILES)
    root = make_di_exports(tmp_path / "g13_di", pins)
    return pins, root, D.DiExports(root, pins)


def unit(i, state="Plain state about weather.", instructions="Answer the question.", card="Plain card.", options=None, **kw):
    return G.row_units([row(i, state, instructions=instructions, card=card, options=options, **kw)])[0]


def test_wording8_flags_a_shared_instruction_8gram_and_nothing_else(di_world):
    _p, _root, ex = di_world
    hit = unit(0, instructions="Please " + DI_WORDING.lower() + " thanks")
    card_hit = unit(1, card="Definitions: " + DI_WORDING)
    clean = unit(2, instructions="Decide whether the claim is supported by the passages")           # 7-word overlap: no 8-gram
    state_only = unit(3, state=DI_WORDING)                                                          # state is the engine's, not wording
    hits, rep = D.di_hits([hit, card_hit, clean, state_only], ex)
    w8 = hits["di03_public"]["wording8"]
    assert set(w8) == {"c0", "c1"} and w8["c0"] == {"instructions"} and w8["c1"] == {"card"}
    assert rep["di03_public.wording8"] == 2
    tpl = {"key": "pool:x#1", "template": True, "texts": [("pool", "Intro {NAME}. " + DI_WORDING)], "rows_src": []}
    assert set(D.di_hits([tpl], ex)[0]["di03_public"]["wording8"]) == {"pool:x#1"}                 # a pool template is a wording


def test_record_ids_match_question_claim_and_tweet_texts_and_the_hover_uid_and_group(di_world):
    _p, _root, ex = di_world
    gsm = unit(0, state=GSM_Q)
    embedded = unit(1, state="Intro line.\n" + GSM_Q + "\nTrailing line.")
    sentence = unit(2, state="Some context first. " + HOVER_CLAIM + ". Then more.")
    tweet = unit(3, state="Tweet:\n" + TWEET.upper())                                              # on its own line (the engine's substring method covers the rest)
    by_uid = unit(4, meta={"uid": "uid-hover-1"})
    by_group = unit(5, meta={"hpqa_id": "hpqa-77"})
    clean = unit(6, state="A clean state about the garden fence and the weather in spring, long enough.", meta={"uid": "other"})
    hits, rep = D.di_hits([gsm, embedded, sentence, tweet, by_uid, by_group, clean], ex)
    rid = hits["di_src_splits"]["record_id"]
    assert set(rid) == {"c0", "c1", "c2", "c3", "c4", "c5"} and rid["c4"] == {"meta.uid"} and rid["c5"] == {"meta.hpqa_id"}
    assert "state" in rid["c1"] and rep["di_src_splits.record_id"] == 6
    short = unit(7, state="Short one")                                                              # < 5 words never matches a text hash
    assert "c7" not in D.di_hits([short], ex)[0].get("di_src_splits", {}).get("record_id", {})


def test_structure_key_of_a_di_request_state_and_options(di_world):
    _p, _root, ex = di_world
    twin = unit(0, state="Mara owes Otto 99 coins after the winter fair closes in the harbour city.", options=["Mara", "Otto"])
    same = unit(1, state=DI_STATE, options=DI_OPTIONS)
    renamed = unit(2, state="Lena owes Kofi 45 coins after the Autumn Fair closes in the Valley Town.", options=["Lena", "Kofi"])
    other = unit(3, state="Quite another state about trains and timetables for the week ahead.", options=["a", "b"])
    hits, _ = D.di_hits([twin, same, renamed, other], ex)
    st = hits["di03_public"]["structure"]
    assert "c1" in st and "c3" not in st and st["c1"] == {"state+options"}
    assert g.struct_g13(DI_STATE, DI_OPTIONS) == D.request_structs({"state": DI_STATE, "questions": {"q": {"criteria": {"a": "Ravi", "b": "Ines"}}}}).pop()
    assert D.request_structs({"state": {"b": 1, "a": "x"}, "questions": {}}) == set()


def test_request_wording_reads_instructions_and_criteria_only():
    row_ = {"state": "S", "questions": {"q1": {"type": "choice", "instructions": "Pick the best one now",
                                                   "criteria": {"A": "first option text", "B": ["x y", "z"]}},
                                        "q2": {"type": "noul", "instructions": {"a": "nested instruction text"}}},
            "expected": {"q1": "A"}}
    assert sorted(D.request_wording(row_)) == ["first option text", "nested instruction text", "Pick the best one now", "x y", "z"] or \
        set(D.request_wording(row_)) == {"Pick the best one now", "first option text", "x y", "z", "nested instruction text"}
    assert "A" not in set(D.request_wording(row_))                                                  # the gold is not wording


def test_exports_refuse_tampering_other_pins_and_missing_files(tmp_path, di_world):
    pins, root, _ex = di_world
    other = pins_for(REAL_FILES)
    other["di03_public"]["files"][D.DI03_FILES[0]]["sha256"] = "0" * 64                              # the DI file was rebuilt
    with pytest.raises(D.DiError, match="other DI files"):
        D.DiExports(root, other)
    with open(root / "record_ids.json", "a") as f:
        f.write(" ")
    with pytest.raises(D.DiError, match="differs"):
        D.DiExports(root, pins)
    with pytest.raises(D.DiError, match="MANIFEST"):
        D.DiExports(tmp_path / "absent", pins)
    root2 = make_di_exports(tmp_path / "g2", pins)
    man = json.loads((root2 / "MANIFEST.json").read_text())
    man["counts"]["wording8"] += 1
    (root2 / "MANIFEST.json").write_text(json.dumps(man))
    with pytest.raises(D.DiError, match="wording8"):
        D.DiExports(root2, pins)
    root3 = make_di_exports(tmp_path / "g3", pins)
    np.save(root3 / "wording8_u64.npy", np.array([5, 3], np.uint64))                                   # not sorted
    man = json.loads((root3 / "MANIFEST.json").read_text())
    man["files"]["wording8_u64.npy"]["sha256"] = g.sha256_file(root3 / "wording8_u64.npy")
    (root3 / "MANIFEST.json").write_text(json.dumps(man))
    with pytest.raises(D.DiError, match="sorted"):
        D.DiExports(root3, pins)


def test_verify_scanned_compares_the_engines_file_shas_with_the_pins():
    pins = pins_for(REAL_FILES)
    ev = {f: d["sha256"] for t in D.TARGETS for f, d in pins[t]["files"].items()}
    assert D.verify_scanned(ev, pins, require=True) == []
    bad = dict(ev, **{D.DI03_FILES[1]: "1" * 64})
    assert "added-rows.jsonl.gz is not the pinned one" in D.verify_scanned(bad, pins)[0]
    gone = {k: v for k, v in ev.items() if k != D.SRC_FILES[2]}
    assert D.verify_scanned(gone, pins) == [] and "isarcasmeval_test.jsonl was not scanned" in D.verify_scanned(gone, pins, require=True)[0]
    assert D.verify_scanned({}, {}, require=True) == []                                               # no pins: the gap says it already


def test_run_guard_lists_the_di_files_only_for_a_di_run(world):
    sets = {"s": {"block": "T98", "train_shas": {}, "seed_shas": {}, "units": []}}
    plain = G.run_guard("candidates", sets, False)
    withdi = G.run_guard("candidates", sets, True)
    names = lambda gd: {Path(k).name for k in gd.start}                                              # noqa: E731
    assert not {"MANIFEST.json", "di_g13.py"} & names(plain)
    assert {"di_g13.py", "di_pins.json"} <= {p.name for p in G.di_guard_files()}
    assert set(D.DiExports.FILES) <= {p.name for p in G.di_guard_files()}
    assert names(withdi) >= names(plain)


# ---- end to end through G.run (synthetic stand-ins for the two engine targets) --------------------------------------------
@pytest.fixture()
def di_run(world, tmp_path, monkeypatch):
    """The `world` of test_g13_c2 plus stand-in DI engine targets (abs: files in tmp), pins/exports under tmp, DI rows in the candidates."""
    ev = tmp_path / "di_eval"
    ev.mkdir()
    rows = [{"id": "q1", "state": "A bakery sells forty loaves each morning at a fixed price per loaf", "questions": {
        "q": {"type": "choice", "instructions": DI_WORDING, "criteria": {"A": "yes", "B": "no"}}}, "expected": {"q": "A"}}]
    (ev / "di03.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (ev / "src.jsonl").write_text(json.dumps({"question": GSM_Q, "answer": "7 x 12 = 84 #### 84"}) + "\n")
    rel = lambda p: g.rel_of(p)                                                                       # noqa: E731
    files = {"di03_public": [rel(ev / "di03.jsonl")], "di_src_splits": [rel(ev / "src.jsonl")]}
    monkeypatch.setattr(D, "FILES", {k: tuple(v) for k, v in files.items()})
    pins = {"kit": {"commit": "c" * 40}, **{
        t: {"complete": True, "gaps": [D.HLE_GAP] if t == "di03_public" else [],
            "files": {f: {"sha256": g.sha256_file(Path(f))} for f in files[t]}} for t in D.TARGETS}}
    pins_path = tmp_path / "g13_di" / "di_pins.json"
    root = make_di_exports(tmp_path / "g13_di", pins)
    pins_path.write_text(json.dumps(pins))
    monkeypatch.setattr(D, "DI_DIR", root)
    monkeypatch.setattr(D, "PINS", pins_path)
    monkeypatch.setattr(D, "EXPORT_MANIFEST", root / "MANIFEST.json")
    monkeypatch.setattr(D, "hle_accepted", lambda prereg_text=None: True)
    tgs = [g.target(n, [f"abs:{ev / ('di03.jsonl' if n == 'di03_public' else 'src.jsonl')}"], kind="generic", blind=True,
                    fields=D.FIELDS[n], note=D.NOTES[n]) for n in D.TARGETS]
    cand = world["cand"]
    extra = [row(20, "Unrelated state about gardening hoses and tool sheds for the new season.",
                 instructions="Pick one. " + DI_WORDING, call="cw"),
             row(21, GSM_Q, call="cg"),
             row(22, "Another clean state about harbour tides and the fishing fleet this week.", meta={"uid": "uid-hover-1"}, call="cu"),
             row(23, DI_STATE, options=DI_OPTIONS, call="cs"),
             row(24, "A bakery sells forty loaves each morning at a fixed price per loaf", call="ce")]
    cand.write_text(cand.read_text() + "".join(json.dumps(r) + "\n" for r in extra))
    return {"tgs": world["tgs"] + tgs, "world": world, "root": root}


def test_a_candidates_run_with_the_di_targets_drops_whole_units_per_method(di_run):
    w = di_run["world"]
    rec = G.run("candidates", ["T98"], embed=False, side=False, tgs=di_run["tgs"], exports=w["exports"], write=False,
                prereg_text=A38)["c2_cand_T98"]
    by = rec["counts_by_target_and_method"]
    assert {"r20", "r21", "r22", "r23", "r24"} <= set(rec["drop_ids"])
    assert by["di03_public"]["wording8"]["units"] == 1 and by["di03_public"]["structure"]["units"] == 1
    assert by["di_src_splits"]["record_id"]["units"] == 2                                              # the question text and the uid
    assert by["di03_public"]["exact_seg"] or by["di03_public"].get("substring")                       # the engine's methods on the DI request
    assert rec["di"]["status"] == "verified" and rec["di"]["kit"]["commit"] == "c" * 40
    assert rec["engine"]["targets"]["di03_public"]["status"] == "scanned" and rec["engine"]["targets"]["di_src_splits"]["status"] == "scanned"
    assert not any("di_exports" in x or "not scanned" in x or "pinned" in x for x in rec["incomplete_why"]), rec["incomplete_why"]
    json.dumps(rec)


def test_a_run_without_the_di_targets_has_no_di_record_or_keys(world):
    rec = _run(world, "candidates", G.c2_dev_targets())["c2_cand_T98"]
    assert "di" not in rec and not any(t.startswith("di") for t in rec["counts_by_target_and_method"])


def test_broken_exports_or_a_rebuilt_di_file_make_the_log_incomplete(di_run, monkeypatch):
    w = di_run["world"]
    (di_run["root"] / "record_ids.json").write_text("{}")                                             # tampered export
    rec = G.run("candidates", ["T98"], embed=False, side=False, tgs=di_run["tgs"], exports=w["exports"], write=False,
                prereg_text=A38)["c2_cand_T98"]
    assert rec["di"]["status"].startswith("refused") and any(x.startswith("di_exports:") for x in rec["incomplete_why"])
    assert not rec["complete"]


def test_a_scanned_di_file_that_is_not_the_pinned_one_is_flagged(di_run, monkeypatch):
    w = di_run["world"]
    pins = json.loads(D.PINS.read_text())
    f = next(iter(pins["di_src_splits"]["files"]))
    pins["di_src_splits"]["files"][f]["sha256"] = "9" * 64
    D.PINS.write_text(json.dumps(pins))
    rec = G.run("candidates", ["T98"], embed=False, side=False, tgs=di_run["tgs"], exports=w["exports"], write=False,
                prereg_text=A38)["c2_cand_T98"]
    assert any("is not the pinned one" in x for x in rec["incomplete_why"]) or rec["di"]["status"].startswith("refused")
    assert not rec["complete"]
