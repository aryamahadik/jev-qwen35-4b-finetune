"""Tests for the A58 System One Bench leak-check target: sob_g13.py (and, when g13_c2.py carries zed_orch/sob_wiring.patch, its wiring).
Synthetic data (pytest tmp_path) for everything but the "real bench" tests, which read the bench cases ONLY through sob_g13's builder
functions (load_verified_cases / case_unit) and print nothing but counts. No G13 run over the real mix, no network, no Modal. Run from lean/:
  ../.venv/bin/python -B -m pytest -q c2_build/tests/test_sob_g13.py
Tests marked "wired" need g13_c2.py to import sob_g13 (the sob_wiring.patch); they are skipped on the unpatched file.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import c2io  # noqa: E402
import sob_g13 as S  # noqa: E402
import g13_c2 as G  # noqa: E402
from test_g13_c2 import A38, EVAL_SENT, _run, exports, fake_tools, row, world  # noqa: E402,F401  (fixtures of the end-to-end world)

g = G.g
wired = pytest.mark.skipif(not hasattr(G, "sob_g13"), reason="g13_c2.py does not carry the A58 sob wiring yet (zed_orch/sob_wiring.patch)")
REAL_SRC, REAL_LOCK = g.REPO / S.SRC_REL, g.REPO / S.LOCK_REL

# ---- a synthetic bench: every field type of the real one --------------------------------------------------------------------
P1 = "The harbour master closed the old quay on Tuesday because the winter storm had loosened the iron rings along its edge"
H1 = "The quay was shut after storm damage to its mooring rings"
I_NLI = "Decide whether the hypothesis follows from the premise or contradicts it or neither, reading only what is stated above"
D_ENT = "the hypothesis is a plain consequence of the premise as it is written"
D_NEU = "the premise says nothing that settles the hypothesis either way"
D_CON = "the premise rules the hypothesis out in so many words"
TWEET = "honestly the new tram timetable makes my morning commute so much easier than the old one ever did"
I_SENT = "Rate how positive the writer feels about the thing described, using the five levels given below"
LVL = ["very negative and angry throughout", "mostly negative with some relief", "neither positive nor negative overall",
       "mostly positive with a few mild reservations", "very positive and openly delighted"]
PASSAGE = "The river authority publishes flood warnings at six in the morning and again at six in the evening during the wet season"
QUESTION = "does the river authority publish flood warnings twice a day"
I_YN = "Answer true or false for the question using the passage and nothing else you may know"
TD_STATE = {"ticket": {"title": "Printer on the third floor jams every few pages after the firmware update", "owner": "facilities team"},
            "history": ["opened on Monday by the night shift", "reassigned twice before noon on Wednesday"]}
I_TD_A = "Is the ticket ready to be closed without further follow up from the facilities team this week"
D_TD_T = "closing now loses no open work item"
D_TD_F = "an open work item remains on the ticket"
I_TD_B = "Which queue should the ticket be routed to next according to the routing note in the history"
OPT_TD = {"hardware repair": "physical parts need replacing at the site", "software support": "the fault comes from settings or updates",
          "procurement": "a new device must be ordered for the floor"}
GOLD_MARK = "GOLDLABELMARKER"


def make_cases() -> list[dict]:
    return [
        {"suite": "s_nli", "id": "s_nli-0", "state": {"premise": P1, "hypothesis": H1},
         "questions": {"q": {"type": "choice", "instructions": I_NLI, "criteria": {"entailment": D_ENT, "neutral": D_NEU, "contradiction": D_CON}}},
         "gold": {"q": {"type": "choice", "label": "entailment", "note": GOLD_MARK}}},
        {"suite": "s_sent", "id": "s_sent-0", "state": TWEET,
         "questions": {"q": {"type": "score", "instructions": I_SENT, "criteria": LVL}}, "gold": {"q": {"type": "score", "label": 3}}},
        {"suite": "s_yn", "id": "s_yn-0", "state": {"passage": PASSAGE, "question": QUESTION},
         "questions": {"q": {"type": "noul", "instructions": I_YN}}, "gold": {"q": {"type": "noul", "label": "true"}}},
        {"suite": "s_td", "id": "td-0", "workflow": "ticket routing flow for the facilities desk", "state": TD_STATE,
         "questions": {"a": {"type": "noul", "instructions": I_TD_A, "criteria": {"true": D_TD_T, "false": D_TD_F}},
                       "b": {"type": "choice", "instructions": I_TD_B, "criteria": OPT_TD}},
         "gold": {"a": {"type": "noul", "label": "false"}, "b": {"type": "choice", "label": "procurement"}}},
    ]


def write_bench(root: Path, cases=None) -> tuple[Path, Path]:
    cases = make_cases() if cases is None else cases
    root.mkdir(parents=True, exist_ok=True)
    cp, lp = root / "cases.jsonl", root / "data.lock.cases.json"
    cp.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in cases), encoding="utf-8")
    lp.write_text(json.dumps(S.fingerprint(cases), indent=1), encoding="utf-8")
    return cp, lp


@pytest.fixture()
def bench(tmp_path):
    return write_bench(tmp_path / "bench")


@pytest.fixture()
def built(tmp_path, monkeypatch, bench):
    """A synthetic build under tmp: the units file, pins and exports, with the module pointed at them."""
    units = tmp_path / "scan" / "sob_units.jsonl"
    out = tmp_path / "g13_sob"
    rel = g.rel_of(units)
    monkeypatch.setattr(S, "EXPECTED_CASES", 4)
    monkeypatch.setattr(S, "EXPECTED_SUITES", 4)
    monkeypatch.setattr(S, "UNITS_REL", rel)
    monkeypatch.setattr(S, "FILES", {"sob_text": (rel,)})
    monkeypatch.setattr(S, "SOB_DIR", out)
    monkeypatch.setattr(S, "PINS", out / "sob_pins.json")
    monkeypatch.setattr(S, "EXPORT_MANIFEST", out / "MANIFEST.json")
    pins = S.build(bench[0], bench[1], units, out)
    return {"pins": pins, "units": units, "out": out, "rel": rel, "cases": bench[0], "lock": bench[1]}


def units_of(built) -> list[dict]:
    return [json.loads(x) for x in built["units"].read_text(encoding="utf-8").splitlines()]


# ---- the lock check ---------------------------------------------------------------------------------------------------------
def test_a_matching_lock_is_accepted_and_reports_hashes_and_counts_only(bench):
    cases, info = S.load_verified_cases(*bench)
    assert len(cases) == 4 and info["suites"] == {"s_nli": 1, "s_sent": 1, "s_td": 1, "s_yn": 1}
    assert set(info) == {"file_sha256", "lock_sha256", "lock_total_sha256", "suites"} and len(info["file_sha256"]) == 64
    assert S.lock_problems(cases, json.loads(bench[1].read_text())) == []


def test_a_changed_case_is_refused_and_nothing_is_written(tmp_path, bench):
    cases = make_cases()
    cases[1]["state"] = TWEET + " today"                                            # one word differs from the frozen case
    cp = tmp_path / "other" / "cases.jsonl"
    cp.parent.mkdir()
    cp.write_text("".join(json.dumps(c) + "\n" for c in cases))
    with pytest.raises(S.SobError, match="do not match their lock") as e:
        S.load_verified_cases(cp, bench[1])
    assert "s_sent" in str(e.value) and TWEET not in str(e.value)                    # suite name and hash prefixes, never the text
    units, out = tmp_path / "u.jsonl", tmp_path / "o"
    with pytest.raises(S.SobError):
        S.build(cp, bench[1], units, out)
    assert not units.exists() and not out.exists()


@pytest.mark.parametrize("how", ["missing_suite", "extra_suite", "bad_total", "no_lock", "no_cases", "not_json", "dup_ids"])
def test_every_kind_of_mismatch_is_refused(tmp_path, bench, how):
    cp, lp = bench
    cases, lock = make_cases(), json.loads(lp.read_text())
    if how == "missing_suite":
        cases = cases[:-1]
    elif how == "extra_suite":
        cases = cases + [dict(cases[0], suite="s_new", id="s_new-0")]
    elif how == "bad_total":
        lock["sha256"] = "0" * 64
    elif how == "dup_ids":
        cases = cases + [dict(cases[0])]
        lock = S.fingerprint(cases)                                                  # even a lock that matches cannot make duplicate ids a bench
    if how in ("missing_suite", "extra_suite", "bad_total", "dup_ids"):
        cp = tmp_path / "x_cases.jsonl"
        cp.write_text("".join(json.dumps(c) + "\n" for c in cases))
        lp = tmp_path / "x_lock.json"
        lp.write_text(json.dumps(lock))
    elif how == "no_lock":
        lp = tmp_path / "absent.json"
    elif how == "no_cases":
        cp = tmp_path / "absent.jsonl"
    else:
        cp = tmp_path / "junk.jsonl"
        cp.write_text("this is not json\n")
    with pytest.raises(S.SobError):
        S.load_verified_cases(cp, lp)


def test_the_fingerprint_is_the_text_track_lockcheck_one(bench):
    """sob_g13.fingerprint is vision_bench/text_track/harness/lockcheck.fingerprint (checked against its source when the bench is there)."""
    lc = g.REPO / "vision_bench/text_track/harness/lockcheck.py"
    if not lc.is_file():
        pytest.skip("text_track harness not present")
    import importlib.util
    spec = importlib.util.spec_from_file_location("tt_lockcheck_for_test", lc)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    assert m.fingerprint(bench[0]) == S.fingerprint(make_cases())
    assert m.check(bench[0], bench[1]) == []


# ---- the units --------------------------------------------------------------------------------------------------------------
def test_one_unit_per_case_with_the_bench_case_id_as_call_id(built):
    us = units_of(built)
    assert [u["call_id"] for u in us] == ["s_nli-0", "s_sent-0", "s_yn-0", "td-0"] and len({u["call_id"] for u in us}) == len(make_cases())
    assert built["pins"]["sob_text"]["complete"] is True and built["pins"]["sob_text"]["gaps"] == []
    assert built["pins"]["sob_text"]["files"][built["rel"]]["rows"] == 4


def test_every_field_type_is_covered_as_a_string_value(built):
    us = {u["call_id"]: u for u in units_of(built)}
    nli, sent, yn, td = us["s_nli-0"], us["s_sent-0"], us["s_yn-0"], us["td-0"]
    # state: a dict state as the model-visible JSON text and as each of its string values; a string state as is
    assert nli["state"] == json.dumps({"premise": P1, "hypothesis": H1}, ensure_ascii=False, indent=1)
    assert sorted(nli["state_values"].values()) == sorted([P1, H1]) and "state_values" not in sent and sent["state"] == TWEET
    assert {*td["state_values"].values()} >= {TD_STATE["ticket"]["title"], "facilities team", *TD_STATE["history"]}     # nested dict and list leaves
    # instructions: one per question; criteria: dict values (choice descriptions, true / false definitions) and list levels
    assert nli["instructions"] == {"q0": I_NLI} and set(td["instructions"].values()) == {I_TD_A, I_TD_B}
    assert sorted(nli["criteria"]["q0"].values()) == sorted([D_ENT, D_NEU, D_CON])
    assert sorted(td["criteria"]["q0"].values()) == sorted([D_TD_T, D_TD_F]) and sorted(td["criteria"]["q1"].values()) == sorted(OPT_TD.values())
    assert list(sent["criteria"]["q0"].values()) == LVL and "criteria" not in yn
    # options: choice option names (the dict KEYS the engine's reader would never see) and the score options in C1's "<i>: <level>" form
    assert sorted(nli["options"]["q0"].values()) == ["contradiction", "entailment", "neutral"]
    assert sorted(td["options"]["q1"].values()) == sorted(OPT_TD) and "q0" not in td["options"]
    assert list(sent["options"]["q0"].values()) == [f"{i}: {v}" for i, v in enumerate(LVL)]
    assert "options" not in yn
    # the definitions card as tt_core.to_row renders it
    assert nli["card"]["q0"] == f"- entailment: {D_ENT}\n- neutral: {D_NEU}\n- contradiction: {D_CON}"
    assert td["card"]["q0"] == f"- Yes: {D_TD_T}\n- No: {D_TD_F}" and td["card"]["q1"].startswith("- hardware repair: ")
    assert "card" not in sent and "card" not in yn
    assert td["workflow"] == "ticket routing flow for the facilities desk" and "workflow" not in nli
    # the gold and the ids' siblings are never written
    blob = built["units"].read_text(encoding="utf-8")
    assert GOLD_MARK not in blob and '"gold"' not in blob
    assert S.coverage_problems(make_cases(), units_of(built)) == []


def test_coverage_problems_see_a_dropped_part():
    cases = make_cases()
    us = [S.case_unit(c) for c in cases]
    assert S.coverage_problems(cases, us) == []
    del us[0]["options"]
    del us[3]["instructions"]["q1"]
    us[1].pop("criteria")
    probs = " | ".join(S.coverage_problems(cases, us))
    assert "options" in probs and "instructions" in probs and "criteria" in probs
    assert "one unit per case" in S.coverage_problems(cases, us[:3])[0]
    assert "one unit per case" in S.coverage_problems(cases, [us[1], us[0], us[2], us[3]])[0]


def test_unit_counts_cover_all_field_kinds(built):
    c = S.unit_counts(units_of(built))
    assert c["units"] == 4 and c["units_with_state"] == 4 and c["units_with_instructions"] == 4
    for f in ("state_values", "criteria", "options", "card", "workflow"):
        assert c[f"units_with_{f}"] >= 1, f


def test_a_build_with_the_wrong_counts_is_incomplete_not_silent(tmp_path, bench):
    units, out = tmp_path / "u.jsonl", tmp_path / "o"
    pins = S.build(bench[0], bench[1], units, out)["sob_text"]                      # EXPECTED_CASES is the real 3,250
    assert pins["complete"] is False and any("3250 expected" in x for x in pins["gaps"]) and any("16 expected" in x for x in pins["gaps"])
    assert S.gap_for("sob_text", {"sob_text": pins}) and "incomplete" in S.gap_for("sob_text", {"sob_text": pins})


# ---- the exports hold no bench text ----------------------------------------------------------------------------------------
def test_pins_and_exports_hold_no_plain_bench_text(built):
    texts = {s for u in units_of(built) for f in S.ROW_FIELDS for s in S._strings(u.get(f)) if len(s) >= 12}
    assert len(texts) > 15
    for name in ("sob_pins.json", "MANIFEST.json", "unit_hashes.json"):
        body = (built["out"] / name).read_text(encoding="utf-8")
        assert not [t for t in texts if t in body], name
    h = json.loads((built["out"] / "unit_hashes.json").read_text())
    assert set(h) == {"s_nli-0", "s_sent-0", "s_yn-0", "td-0"} and all(re.fullmatch(r"[0-9a-f]{64}", v) for v in h.values())
    assert built["units"].read_text(encoding="utf-8").count(P1) >= 1                  # the one file with bench text is the units file


def test_pin_record_names_source_lock_and_units_by_sha(built, bench):
    p = built["pins"]["sob_text"]
    assert p["source"]["file_sha256"] == S.sha_bytes(bench[0].read_bytes()) and p["source"]["lock_sha256"] == S.sha_bytes(bench[1].read_bytes())
    assert p["source"]["cases"] == 4 and p["source"]["questions"] == 5
    assert p["files"][built["rel"]]["sha256"] == g.sha256_file(built["units"])
    assert S.gap_for("sob_text", {"sob_text": p}) is None and S.complete({"sob_text": p})
    assert S.pinned_files({"sob_text": p}) == {built["rel"]: g.sha256_file(built["units"])}


def test_gap_for_needs_a_complete_pin_that_pins_the_units_and_the_source(built):
    p = built["pins"]["sob_text"]
    assert "not built yet" in S.gap_for("sob_text", {})
    assert "not complete" in S.gap_for("sob_text", {"sob_text": dict(p, complete=False)}) or "incomplete" in S.gap_for("sob_text", {"sob_text": dict(p, complete=False)})
    assert "incomplete" in S.gap_for("sob_text", {"sob_text": dict(p, gaps=["x"])})
    assert "does not pin the units" in S.gap_for("sob_text", {"sob_text": dict(p, files={})})
    assert "does not pin the units" in S.gap_for("sob_text", {"sob_text": dict(p, files={built["rel"]: {"rows": 4}})})
    assert "source sha256" in S.gap_for("sob_text", {"sob_text": dict(p, source={})})
    assert not S.complete({})


def test_exports_refuse_tampering_other_pins_and_missing_files(tmp_path, built):
    pins, out = {"sob_text": built["pins"]["sob_text"]}, built["out"]
    ex = S.SobExports(out, pins)
    assert len(ex.unit_hashes) == 4 and ex.counts["units"] == 4 and set(ex.shas) == {"manifest", "unit_hashes.json"}
    assert S.units_file_problems(built["units"], ex) == []
    other = json.loads(json.dumps(pins))
    other["sob_text"]["files"][built["rel"]]["sha256"] = "0" * 64                     # the units file was rebuilt
    with pytest.raises(S.SobError, match="another units file"):
        S.SobExports(out, other)
    with pytest.raises(S.SobError, match="MANIFEST"):
        S.SobExports(tmp_path / "absent", pins)
    import shutil
    for kind in ("tamper", "count"):
        d = tmp_path / kind
        shutil.copytree(out, d)
        if kind == "tamper":
            with open(d / "unit_hashes.json", "a") as f:
                f.write(" ")
            with pytest.raises(S.SobError, match="differs"):
                S.SobExports(d, pins)
        else:
            man = json.loads((d / "MANIFEST.json").read_text())
            man["counts"]["units"] += 1
            (d / "MANIFEST.json").write_text(json.dumps(man))
            with pytest.raises(S.SobError, match="MANIFEST.json says"):
                S.SobExports(d, pins)


def test_a_changed_units_file_is_found_against_the_exports(built):
    ex = S.SobExports(built["out"], {"sob_text": built["pins"]["sob_text"]})
    us = units_of(built)
    us[0]["state"] += " edited"
    built["units"].write_text("".join(json.dumps(u) + "\n" for u in us))
    assert "1 units differ" in " ".join(S.units_file_problems(built["units"], ex))
    built["units"].write_text("".join(json.dumps(u) + "\n" for u in us[:3]))
    assert "lacks 1 of its units" in " ".join(S.units_file_problems(built["units"], ex))
    assert S.units_file_problems(built["units"].parent / "absent", ex)[0].startswith("the units file is not readable")


def test_verify_scanned_compares_the_engines_file_sha_with_the_pin(built):
    pins = {"sob_text": built["pins"]["sob_text"]}
    sha = g.sha256_file(built["units"])
    assert S.verify_scanned({built["rel"]: sha}, pins, require=True) == []
    assert "is not the pinned one" in S.verify_scanned({built["rel"]: "1" * 64}, pins)[0]
    assert S.verify_scanned({}, pins) == [] and "was not scanned" in S.verify_scanned({}, pins, require=True)[0]
    assert S.verify_scanned({}, {}, require=True) == []                               # no pins: the gap says it already


# ---- registration ------------------------------------------------------------------------------------------------------------
def test_the_units_file_is_readable_by_the_engine_without_an_allow_list_entry():
    assert S.QUARANTINE_OK == () and S.engine_allows() and g.allowed(g.REPO / S.UNITS_REL)
    before = tuple(g.QUARANTINE_OK)
    S.patch_engine()
    S.patch_engine()
    assert tuple(g.QUARANTINE_OK) == before                                           # idempotent, and nothing to add
    assert not g.allowed(g.REPO / "bench/external_quarantine/sob/other.jsonl")
    assert c2io.refusal(g.REPO / S.UNITS_REL) is None and not c2io.refusal(S.PINS)
    parts = [x.lower() for x in Path(S.UNITS_REL).parts]
    assert not any("ohs" in x or "jev" in x or "sealed" in x for x in parts) and not any(x in ("runs", "results", "_work", "preds") for x in parts)


def test_the_target_dict_is_blind_generic_all_methods_with_the_unit_fields(built):
    t, = S.targets({"sob_text": built["pins"]["sob_text"]})
    assert t["name"] == "sob_text" and t["blind"] is True and t["kind"] == "generic" and t["methods"] == "all" and t["status"] is None
    assert t["paths"] == ["repo:" + built["rel"]] and t["fields"] == S.FIELDS and t["gap"] is None and t["note"] == S.NOTES["sob_text"]
    assert set(S.FIELDS) == set(S.ROW_FIELDS) and "call_id" not in S.FIELDS and "suite" not in S.FIELDS and "gold" not in S.FIELDS
    assert S.targets({})[0]["gap"] and "not built yet" in S.targets({})[0]["gap"]       # nothing pinned: the target is incomplete
    di_like = {x["name"]: x for x in g.targets()}["di_test"]
    assert set(t) == set(di_like)                                                   # the same dict shape as every engine target


def test_the_dictionary_keys_are_not_what_the_engine_reads_so_the_unit_file_carries_them_as_values(built):
    """The engine's leaves() reads string values only: the choice options (dict keys) must be values in the file."""
    us = units_of(built)
    leaves = [x for u in us for x in g.leaves(u, S.FIELDS)]
    for opt in ("entailment", "contradiction", "hardware repair", "procurement"):
        assert opt in leaves
    assert D_ENT in leaves and I_TD_B in leaves and f"3: {LVL[3]}" in leaves
    assert not [x for x in leaves if x in ("s_nli-0", "td-0", "s_nli", GOLD_MARK)]   # ids, suite names and gold are not read


# ---- needs_sob: which runs hold the target ---------------------------------------------------------------------------------
def test_needs_sob_follows_the_run_and_the_blocks():
    cand = lambda b, u=(): {"c2_cand_" + b: {"block": b, "units": list(u)}}          # noqa: E731
    units_sb5 = [{"rows_src": [{"meta": {"family": "SB5"}}]}]
    units_di = [{"rows_src": [{"meta": {"family": "DI-TS"}}]}]
    units_core = [{"rows_src": [{"meta": {"family": "T28"}}, {"meta": None}, {}]}]
    final = lambda u: {"c2_final": {"block": "final", "units": u}}                    # noqa: E731
    assert S.needs_sob("final", final(units_core)) and S.needs_sob("final", {})        # every final all-block run
    assert S.needs_sob("candidates", cand("SB5")) and S.needs_sob("candidates", cand("DI-KR")) and S.needs_sob("carry", cand("DI-LANG"))
    assert S.needs_sob("candidates", cand("T28", units_sb5)) and S.needs_sob("candidates", cand("T28", units_di))
    assert not S.needs_sob("candidates", cand("T28", units_core)) and not S.needs_sob("candidates", cand("GB"))
    assert not S.needs_sob("carry", cand("F5"))
    assert not S.needs_sob("seed", cand("SB5")) and not S.needs_sob("seed", cand("DI-TS", units_di)) and not S.needs_sob("seed", cand("T28"))
    assert S.has_sob_rows(units_sb5) and S.has_sob_rows(units_di) and not S.has_sob_rows(units_core)
    assert set(S.SOB_BLOCKS) == {"SB5", *c2io.DI_BLOCKS}


# ---- the engine finds a planted bench text (positive control) and leaves clean rows alone (negative control) -------------------
@pytest.fixture()
def sob_run(world, built, monkeypatch):
    """The `world` of test_g13_c2 plus the synthetic bench units as an `abs:` engine target, with SOB rows planted in the candidates."""
    pins = {"sob_text": built["pins"]["sob_text"]}
    t, = S.targets(pins)
    t["paths"] = [f"abs:{built['units']}"]
    cand = world["cand"]
    state_json = json.dumps(TD_STATE, ensure_ascii=False, indent=1)
    extra = [row(30, "Daily notes. " + P1 + ". End of notes.", call="p_state_value"),                    # a bench state value inside a longer state
             row(31, "Another clean state about harbour tides and the fishing fleet this week.", instructions="Task: " + I_NLI, call="p_instr"),
             row(32, "Clean state number thirty two about garden hoses and tool sheds.", card="- neutral: " + D_NEU, call="p_card"),
             row(33, "Clean state number thirty three about bread and the village oven.", options=["1: x y z", f"3: {LVL[3]}"], call="p_score_option"),
             row(34, state_json, call="p_state_json"),
             row(35, "Ticket history says " + TD_STATE["history"][1] + " according to the log.", call="p_state_list_leaf"),
             row(36, "Clean state number thirty six about a bakery that sells forty loaves each morning at a fixed price.", call="clean_a"),
             row(37, "A different story entirely: the lighthouse keeper repainted the railings before the first frost came.", call="clean_b",
                 instructions="Say which of the two ferry timetables is faster.", card="- fast: the ferry that stops less often")]
    cand.write_text(cand.read_text() + "".join(json.dumps(r) + "\n" for r in extra))
    return {"world": world, "tgs": world["tgs"] + [t], "pins": pins, "target": t}


def _cand(sob_run, **kw):
    w = sob_run["world"]
    return G.run("candidates", ["T98"], embed=False, side=False, tgs=sob_run["tgs"], exports=w["exports"], write=False, prereg_text=A38, **kw)["c2_cand_T98"]


def test_a_planted_bench_text_is_found_by_the_target_and_clean_rows_are_not(sob_run):
    rec = _cand(sob_run)
    planted = {"r30", "r31", "r32", "r33", "r34", "r35"}
    assert planted <= set(rec["drop_ids"]), sorted(planted - set(rec["drop_ids"]))
    assert not {"r36", "r37"} & set(rec["drop_ids"])                                   # negative control: unrelated rows keep
    by = rec["counts_by_target_and_method"]["sob_text"]
    assert sum(1 for c in by.values() if c["units"] >= 1) >= 2                          # more than one method sees them
    assert max(c["units"] for c in by.values()) >= 6                                    # the six planted units, whichever method counts them
    assert rec["engine"]["targets"]["sob_text"]["status"] == "scanned"
    json.dumps(rec)                                                                    # the record is JSON and holds no bench text
    assert P1 not in json.dumps(rec) and I_NLI not in json.dumps(rec)


def test_a_run_whose_rows_never_touch_the_bench_has_no_sob_hits(world, built):
    pins = {"sob_text": built["pins"]["sob_text"]}
    t, = S.targets(pins)
    t["paths"] = [f"abs:{built['units']}"]
    rec = G.run("candidates", ["T98"], embed=False, side=False, tgs=world["tgs"] + [t], exports=world["exports"], write=False,
                prereg_text=A38)["c2_cand_T98"]
    assert "sob_text" not in rec["counts_by_target_and_method"]                         # the stock rows hit other targets, none hits the bench
    assert rec["engine"]["targets"]["sob_text"]["status"] == "scanned"


def test_the_engine_reads_the_options_the_unit_file_carries(world, built):
    """A row that repeats the five-plus-word 'i: level' score option form of a bench case is found (the option strings are in the units)."""
    pins = {"sob_text": built["pins"]["sob_text"]}
    t, = S.targets(pins)
    t["paths"] = [f"abs:{built['units']}"]
    w = world
    w["cand"].write_text(w["cand"].read_text() + json.dumps(
        row(40, "Clean state number forty about a quiet street market in the early morning.", options=[f"0: {LVL[0]}", f"4: {LVL[4]}"])) + "\n")
    rec = G.run("candidates", ["T98"], embed=False, side=False, tgs=w["tgs"] + [t], exports=w["exports"], write=False,
                prereg_text=A38)["c2_cand_T98"]
    assert "r40" in rec["drop_ids"] and "sob_text" in rec["counts_by_target_and_method"]


# ---- the wiring (needs the patched g13_c2.py) --------------------------------------------------------------------------------
@wired
def test_wired_engine_targets_gain_exactly_the_sob_target_only_when_asked(monkeypatch, tmp_path):
    monkeypatch.setattr(S, "PINS", tmp_path / "no_pins.json")
    monkeypatch.setattr(S, "SPLITS_PINS", tmp_path / "no_splits_pins.json")
    base = {t["name"] for t in G.engine_targets("final")}
    assert "sob_text" not in base and "sob_text" not in {t["name"] for t in G.engine_targets("seed")}
    for run in ("seed", "candidates", "carry", "final"):
        b = {t["name"] for t in G.engine_targets(run)}
        assert {t["name"] for t in G.engine_targets(run, False, True)} == b | {"sob_text", "sob_splits"}, run       # A58 step 12: the full-splits target joins with it
        assert {t["name"] for t in G.engine_targets(run, True, True)} >= b | {"sob_text", "sob_splits", "di03_public", "di_src_splits"}, run
    assert [t for t in G.engine_targets("final", False, True) if t["name"] == "sob_text"][0]["gap"]       # no pins: incomplete


@wired
def test_wired_run_guard_lists_the_sob_files_only_for_a_sob_run(world):
    sets = {"s": {"block": "T98", "train_shas": {}, "seed_shas": {}, "units": []}}
    names = lambda gd: {Path(k).name for k in gd.start}                                              # noqa: E731
    plain, withsob = names(G.run_guard("candidates", sets, False)), names(G.run_guard("candidates", sets, False, True))
    assert not {"sob_g13.py", "sob_pins.json", "unit_hashes.json", Path(S.UNITS_REL).name} & plain
    assert {"sob_g13.py", "sob_pins.json", "MANIFEST.json", "unit_hashes.json", Path(S.UNITS_REL).name} <= withsob
    assert plain <= withsob and not {"sob_g13.py", "sob_pins.json"} & names(G.run_guard("candidates", sets, True, False))    # a DI-only run adds the DI files only


@wired
def test_wired_a_run_with_the_target_records_verified_exports_and_complete_pins(sob_run, built, monkeypatch):
    rec = _cand(sob_run)
    assert rec["sob"]["status"] == "verified" and rec["sob"]["units"] == 4 and set(rec["sob"]["sha256"]) == {"manifest", "unit_hashes.json"}
    assert rec["sob"]["source"]["file_sha256"] == built["pins"]["sob_text"]["source"]["file_sha256"]
    assert not any("sob_" in x or "pinned" in x for x in rec["incomplete_why"]), rec["incomplete_why"]
    assert sorted(rec["inputs_at_start"]) and any(Path(k).name == "sob_g13.py" for k in rec["inputs_at_start"])
    json.dumps(rec)


@wired
def test_wired_a_run_without_the_target_has_no_sob_key(world):
    rec = _run(world, "candidates", G.c2_dev_targets())["c2_cand_T98"]
    assert "sob" not in rec and "sob_text" not in rec["counts_by_target_and_method"]


@wired
def test_wired_broken_exports_or_a_rebuilt_units_file_make_the_log_incomplete(sob_run, built):
    (built["out"] / "unit_hashes.json").write_text("{}")                                             # tampered export
    rec = _cand(sob_run)
    assert rec["sob"]["status"].startswith("refused") and any(x.startswith("sob_exports:") for x in rec["incomplete_why"])
    assert not rec["complete"]


@wired
def test_wired_a_scanned_units_file_that_is_not_the_pinned_one_is_flagged(sob_run, built):
    pins = json.loads(S.PINS.read_text())
    pins["sob_text"]["files"][built["rel"]]["sha256"] = "9" * 64
    S.PINS.write_text(json.dumps(pins))
    rec = _cand(sob_run)
    assert (any("is not the pinned one" in x for x in rec["incomplete_why"]) or rec["sob"]["status"].startswith("refused")) and not rec["complete"]


@wired
def test_wired_an_unbuilt_target_keeps_the_log_incomplete(world, tmp_path, monkeypatch):
    monkeypatch.setattr(S, "PINS", tmp_path / "none.json")
    t, = S.targets()
    t["paths"] = []
    rec = G.run("candidates", ["T98"], embed=False, side=False, tgs=world["tgs"] + [t], exports=world["exports"], write=False,
                prereg_text=A38)["c2_cand_T98"]
    assert not rec["complete"] and any("sob_text: not built yet" in x for x in rec["incomplete_why"])


@wired
def test_wired_the_final_run_holds_the_target_by_default_and_a_seed_run_does_not(world, tmp_path):
    """Default targets (tgs=None) against the REAL pins and units file (the engine reads them; only counts are asserted)."""
    if not S.complete() or not (g.REPO / S.UNITS_REL).is_file():
        pytest.skip("sob_g13.py build has not been run here")
    final = c2io.C2_PARTS / "c2_train.jsonl"
    final.write_text(json.dumps(row(0, "Replay row about the canteen menu and the prices for next week at noon.")) + "\n")
    rec = G.run("final", [], embed=False, side=False, exports=world["exports"], write=False, prereg_text=A38)["c2_final"]
    assert rec["engine"]["targets"]["sob_text"]["status"] == "scanned" and rec["sob"]["status"] == "verified"
    assert rec["sob"]["units"] == S.EXPECTED_CASES == 3250 and "r0" not in rec["drop_ids"]
    assert not any("sob_text" in x or "sob_exports" in x for x in rec["incomplete_why"]), rec["incomplete_why"]
    if S.gap_for("sob_splits") is None:                                                            # A58 step 12: the full-splits target is built: nothing of the SOB targets is open
        assert not any("sob_" in x for x in rec["incomplete_why"]) and rec["sob_splits"]["status"] == "verified"
    else:                                                                                          # not built: the log says so (and only that) until build-splits has run
        assert any("sob_splits: not built yet" in x for x in rec["incomplete_why"]) and not rec["complete"]
    assert rec["engine"]["inputs_sha256"]["eval"][S.UNITS_REL] == S.load_pins()["sob_text"]["files"][S.UNITS_REL]["sha256"]
    seed = G.run("seed", ["T98"], embed=False, side=False, tgs=world["tgs"], exports=world["exports"], write=False, prereg_text=A38)["c2_seed_T98"]
    assert "sob" not in seed
    assert "sob_text" not in {t["name"] for t in G.engine_targets("seed")}


# ---- the real bench (read through the builder only; counts and shas only) ----------------------------------------------------
@pytest.mark.skipif(not (REAL_SRC.is_file() and REAL_LOCK.is_file()), reason="the bench cases are not here")
def test_the_real_bench_matches_its_lock_and_gives_3250_units_with_every_field_type():
    cases, info = S.load_verified_cases()
    us = [S.case_unit(c) for c in cases]
    assert len(us) == 3250 == S.EXPECTED_CASES == sum(info["suites"].values()) and len(info["suites"]) == 16 == S.EXPECTED_SUITES
    assert len({u["call_id"] for u in us}) == 3250 and [u["call_id"] for u in us] == [c["id"] for c in cases]
    assert S.coverage_problems(cases, us) == []
    c = S.unit_counts(us)
    assert c["units"] == 3250 and c["units_with_state"] == 3250 and c["units_with_instructions"] == 3250 and c["units_with_state_values"] == 3250
    assert c["strings_instructions"] == sum(len(x["questions"]) for x in cases) == 4850            # every decision's instruction
    for f in ("criteria", "options", "card", "workflow"):
        assert c[f"units_with_{f}"] > 0, f
    assert c["units_with_workflow"] == 400 and c["units_with_options"] == 2450 and c["units_with_card"] == 2250
    # choice keys (dict keys) and score levels (lists) both reach the units as option strings
    n_choice_keys = sum(len(q["criteria"]) for x in cases for q in x["questions"].values() if q["type"] == "choice")
    n_score_levels = sum(len(q["criteria"]) for x in cases for q in x["questions"].values() if q["type"] == "score")
    assert c["strings_options"] == n_choice_keys + n_score_levels
    assert all(set(u) <= {"call_id", "suite", *S.FIELDS} for u in us) and not any("gold" in u for u in us)


@pytest.mark.skipif(not (REAL_SRC.is_file() and REAL_LOCK.is_file()) or not S.complete(), reason="the bench cases are not here or sob_g13.py build has not been run")
def test_real_bench_text_planted_in_fake_rows_is_found_by_the_real_units_and_clean_rows_are_not(world):
    """Positive / negative control on the REAL units file: a real bench state value, a real model-visible state text and a real definitions card
    are planted in fake rows (never printed: only booleans are asserted)."""
    cases, _ = S.load_verified_cases()
    by_suite = {}
    for c in cases:
        by_suite.setdefault(c["suite"], c)
    boolq_vals = sorted(S._strings(by_suite["boolq"]["state"]), key=len)
    long_val = boolq_vals[-1]
    json_state = S.state_text(by_suite["xnli_en"]["state"])
    card = next(u["card"]["q1"] for u in map(S.case_unit, cases) if u["suite"] == "typed-decisions" and "q1" in (u.get("card") or {}))
    assert len(long_val.split()) >= 12 and len(card.split()) >= 8
    rows = [row(50, "Notes follow. " + long_val + " End of notes.", call="real_state_value"),
            row(51, json_state, call="real_state_json"),
            row(52, "Clean state fifty two about a bakery that sells forty loaves each morning.", card=card, call="real_card"),
            row(53, "Clean state fifty three about ferry timetables and the harbour at dusk this week.", call="clean_a"),
            row(54, "The lighthouse keeper repainted the railings before the first frost came to the bay.", call="clean_b",
                instructions="Say which of the two timetables is faster.", card="- fast: the ferry that stops less often")]
    world["cand"].write_text(world["cand"].read_text() + "".join(json.dumps(r) + "\n" for r in rows))
    t, = S.targets()
    rec = G.run("candidates", ["T98"], embed=False, side=False, tgs=world["tgs"] + [t], exports=world["exports"], write=False,
                prereg_text=A38)["c2_cand_T98"]
    drop = set(rec["drop_ids"])
    found = {"r50", "r51", "r52"} <= drop
    clean = not ({"r53", "r54"} & drop)
    scanned = rec["engine"]["targets"]["sob_text"]["status"] == "scanned"
    assert found and clean and scanned


@pytest.mark.skipif(not (REAL_SRC.is_file() and REAL_LOCK.is_file()), reason="the bench cases are not here")
def test_the_real_pins_and_exports_are_consistent_and_hold_no_bench_text():
    pins = S.load_pins()
    if not pins:
        pytest.skip("sob_g13.py build has not been run here")
    p = pins["sob_text"]
    assert S.gap_for("sob_text", pins) is None and p["complete"] is True and p["gaps"] == [] and S.complete(pins)
    f = g.REPO / S.UNITS_REL
    assert p["files"][S.UNITS_REL] == {"rows": 3250, "sha256": g.sha256_file(f)}
    assert p["source"]["file_sha256"] == g.sha256_file(REAL_SRC) and p["source"]["lock_sha256"] == g.sha256_file(REAL_LOCK)
    assert p["source"]["cases"] == 3250 and p["source"]["questions"] == 4850 and sum(p["source"]["suites"].values()) == 3250
    ex = S.SobExports(pins=pins)
    assert len(ex.unit_hashes) == 3250 and S.units_file_problems(f, ex) == []
    cases, _ = S.load_verified_cases()
    texts = {s for u in (S.case_unit(c) for c in cases) for fld in S.ROW_FIELDS if fld != "workflow" for s in S._strings(u.get(fld)) if len(s) >= 24}   # (a workflow name is part of a typed-decisions case id)
    assert len(texts) > 1000
    body = "\n".join((S.SOB_DIR / n).read_text(encoding="utf-8") for n in ("sob_pins.json", "MANIFEST.json", "unit_hashes.json"))
    assert not [t for t in texts if t in body]                                                     # no plain bench text in g13_sob/
    assert S.units_file_problems(f, ex) == [] and [t for t in S.targets(pins)] and S.targets(pins)[0]["gap"] is None
