"""Tests for owner option 2: (a) frame_excuse.py, (b) keyword_rule.py + keyword_narrow.py, and the launcher opt2_launch.py. Synthetic data only
(synthetic family folders under tmp_path, synthetic hash sets built with g13_c2's own hash functions, a FAKE OHS-AC side and fake OHS-AC
checkers defined here). No sealed, "ohs" or Jev path is opened; the real PREREG_FINAL.md is read (a C2-side doc) by one test. Run from lean/:
  ../.venv/bin/python -B -m pytest -q c2_build/zed_orch/owner_options/tests/test_opt2_frame_and_keywords.py
"""
from __future__ import annotations

import json
import sys
import types
from collections import defaultdict
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
OPT = Path(__file__).resolve().parents[1]
C2B = OPT.parents[1]
for p in (str(OPT), str(C2B), str(C2B / "tests")):
    sys.path.insert(0, p)
import c2io  # noqa: E402
import frame_excuse as fe  # noqa: E402
import g13_c2 as G  # noqa: E402
import keyword_narrow as kn  # noqa: E402
import keyword_rule as kr  # noqa: E402
import opt2_launch as launch  # noqa: E402
import ruling_gate as rg  # noqa: E402
from test_g13_c2 import SUITE_HOST, SUITE_KEYWORD, exports, row  # noqa: E402,F401

PREREG = ("> **Ruling A70 (owner decision in chat, 17 Oct 2026; orchestrator).** own frame text is excused.\n> Machine marker: OHSAC_FRAME_EXCUSE.\n\n"
          "> **Ruling A71 (owner decision in chat; orchestrator).** use the narrowed keyword export.\n> Machine marker: OHSAC_KW_NARROW.\n\n"
          "> **Ruling A72 (owner decision; orchestrator).** both together.\n> Machine marker: OHSAC_FRAME_EXCUSE, OHSAC_FRAME_POOLS.\n\n"
          "> **Ruling A73 (owner decision; orchestrator).** option 3.\n> Machine marker: OHSAC_REPORT_ONLY.\n")


# ------------------------------------------------------------------------------------------------ the keyword rule
ZIPF = {"router": 3.7, "ledger": 3.6, "quillmoor": 0.4, "vaultkeeper": 1.9, "database": 4.9}


def test_rule_cases():
    z = lambda t: ZIPF.get(t, 0.0)    # noqa: E731
    cases = [("Task Router", True, "multi_token"), ("  quillmoor   freight. ", True, "multi_token"),
             ("tasksource/zero-shot-label-nli", True, "identifier"), ("quillmoor.example", True, "identifier"),
             ("gpt4", True, "identifier"), ("snake_case", True, "identifier"),
             ("Quillmoor", True, "rare_word"), ("vaultkeeper", True, "rare_word"),
             ("router", False, "common_word"), ("ledger", False, "common_word"), ("database", False, "common_word"),
             ("axe", False, "too_short"), ("(ab)", False, "too_short"), ("tool", False, "short_single"), ("zzzz", False, "short_single")]
    for name, keep, why in cases:
        assert kr.decide(name, z) == (keep, why), name
    # zipf is only asked for a plain single token of >= 5 characters (never for multi-token / identifier / short names)
    asked = []
    for name in ("Task Router", "a/b", "tool", "x1"):
        kr.decide(name, lambda t: asked.append(t) or 0.0)
    assert asked == []
    kr.decide("ledger", lambda t: asked.append(t) or 0.0)
    assert asked == ["ledger"]


def test_keyword_rule_matches_format():
    assert kr.KW_STRIP == G.KW_STRIP and kr.EXPORT_MIN_LEN == 4
    assert set(kr.REASONS_KEEP).isdisjoint(kr.REASONS_DROP)


# ------------------------------------------------------------------------------------------------ the narrowed export
def kw_hash(name: str) -> str:
    return G.sha_hex(" ".join(name.lower().split()))


def build_kw(root: Path, full: set, keep: list, parent: str, **over):
    """A synthetic narrowed export folder in the layout of keyword_narrow.py's doc. `over` overrides manifest keys (dotted rule.x allowed)."""
    root.mkdir(parents=True, exist_ok=True)
    hs = sorted(keep)
    (root / "keyword_hashes.jsonl").write_text("".join(json.dumps({"kind": "keyword", "hash": h}) + "\n" for h in hs))
    man = {"kind": kn.KIND, "version": kn.VERSION, "parent_manifest_sha256": parent,
           "files": {"keyword_hashes.jsonl": {"sha256": kn._sha(root / "keyword_hashes.jsonl"), "records": len(hs)}},
           "rule": {"version": kr.RULE_VERSION, "file": "keyword_rule.py", "rule_sha256": kn.rule_sha256(), "min_len_single": kr.SINGLE_MIN_LEN,
                    "zipf_max": kr.ZIPF_MAX, "wordfreq_version": kr.WORDFREQ_VERSION, "export_min_len": kr.EXPORT_MIN_LEN},
           "counts": {"full_keyword_hashes": len(full), "narrowed_hashes": len(hs),
                      "kept_names_by_reason": {"multi_token": 1, "identifier": 1}, "dropped_names_by_reason": {"common_word": 3}}}
    for k, v in over.items():
        if k.startswith("rule."):
            man["rule"][k[5:]] = v
        elif k.startswith("counts."):
            man["counts"][k[7:]] = v
        else:
            man[k] = v
    (root / "MANIFEST.json").write_text(json.dumps(man))
    return root


FULL = {kw_hash(x) for x in ("quillmoor freight", "quillmoor", "freight", "router", "ledger", "quillmoor.example", "www.quillmoor.example")}
KEEP = [kw_hash("quillmoor freight"), kw_hash("quillmoor.example")]
PARENT = "p" * 64


def test_a_good_export_loads_and_reports_counts_only(tmp_path):
    root = build_kw(tmp_path / "kw", FULL, KEEP, PARENT)
    info, hs = kn.load_narrowed(root, FULL, PARENT)
    assert hs == frozenset(KEEP) and info["narrowed_hashes"] == 2 and info["full_keyword_hashes"] == len(FULL)
    assert info["rule_sha256"] == kn.rule_sha256() and info["kept_names_by_reason"] == {"identifier": 1, "multi_token": 1}
    assert not any(h in json.dumps(info) for h in hs)


@pytest.mark.parametrize("what", ["no_files", "kind", "sha", "records", "rule_sha", "rule_value", "wordfreq", "parent", "not_subset",
                                  "empty", "same_size", "bad_reason", "counts_full", "bad_line", "dup"])
def test_a_bad_export_is_refused(tmp_path, what):
    root = tmp_path / "kw"
    over = {}
    keep = list(KEEP)
    if what == "kind":
        over["kind"] = "other"
    if what == "rule_sha":
        over["rule.rule_sha256"] = "0" * 64
    if what == "rule_value":
        over["rule.zipf_max"] = 4.0
    if what == "wordfreq":
        over["rule.wordfreq_version"] = "0.0.1"
    if what == "parent":
        over["parent_manifest_sha256"] = "q" * 64
    if what == "not_subset":
        keep = [KEEP[0], kw_hash("a name that is not in the full export")]
    if what == "empty":
        keep = []
    if what == "same_size":
        keep = sorted(FULL)
        over["counts.kept_names_by_reason"] = {"multi_token": 1}
    if what == "bad_reason":
        over["counts.kept_names_by_reason"] = {"because_i_said_so": 1}
    if what == "counts_full":
        over["counts.full_keyword_hashes"] = 3
    if what == "dup":
        keep = [KEEP[0], KEEP[0]]
    build_kw(root, FULL, keep, PARENT, **over)
    if what == "no_files":
        (root / "MANIFEST.json").unlink()
    if what == "sha":
        (root / "keyword_hashes.jsonl").write_text((root / "keyword_hashes.jsonl").read_text() + "\n")
    if what == "records":
        man = json.loads((root / "MANIFEST.json").read_text())
        man["files"]["keyword_hashes.jsonl"]["records"] = 99
        (root / "MANIFEST.json").write_text(json.dumps(man))
    if what == "bad_line":
        (root / "keyword_hashes.jsonl").write_text(json.dumps({"kind": "text", "hash": "x"}) + "\n")
        man = json.loads((root / "MANIFEST.json").read_text())
        man["files"]["keyword_hashes.jsonl"]["sha256"] = kn._sha(root / "keyword_hashes.jsonl")
        (root / "MANIFEST.json").write_text(json.dumps(man))
    with pytest.raises(kn.NarrowError) as e:
        kn.load_narrowed(root, FULL, PARENT)
    assert "refused" in str(e.value)


def test_narrowing_changes_the_keyword_compare_and_nothing_else(exports):
    """With g13_c2's own compare: the full set hits a lone token, the narrowed set only the multi-token name / the host."""
    full = set(exports.sets["keyword"])
    lone = G.sha_hex("quillmoor")
    exports.sets["keyword"] = full | {lone}
    units = [{"key": "u1", "texts": [("state", "Please ask Quillmoor about the delivery date for the parcel soon.")], "template": False},
             {"key": "u2", "texts": [("state", "Please ask " + SUITE_KEYWORD + " about the delivery date for the parcel.")], "template": False},
             {"key": "u3", "texts": [("state", "Please write to " + SUITE_HOST + " about the delivery date for the parcel.")], "template": False}]
    h1, _ = G.ohs4_hash_hits(units, exports)
    assert set(h1["keyword"]) == {"u1", "u2", "u3"}
    exports.sets["keyword"] = full                                  # narrowed set stand-in: the multi-token name and the host, no lone token
    h2, _ = G.ohs4_hash_hits(units, exports)
    assert set(h2["keyword"]) == {"u2", "u3"}
    assert {m for m in h1} == {m for m in h2} == {"keyword"}        # no other method is affected


class FakeAcSide:
    """Stand-in for g13_c2.AcSide with the surface keyword_narrow.install touches."""
    ex = None

    def __init__(self, ex, union=None):
        self.ex, self.union = ex, union or {"exports": []}

    @classmethod
    def load(cls, root=None, union_root=None, prereg_text=None):
        return cls(FAKE["ex"], FAKE.get("union"))

    def record(self):
        return {"manifest_verified": True}


FAKE: dict = {}


def fake_G(tmp_path):
    return types.SimpleNamespace(AcSide=type("Side", (FakeAcSide,), {}), HERE=tmp_path, ac_guard_files=lambda: [Path("MANIFEST.json")])


def test_install_swaps_the_keyword_set_records_it_and_guards_the_files(tmp_path):
    root = build_kw(tmp_path / "kw", FULL, KEEP, PARENT)
    union_ex = types.SimpleNamespace(sets=defaultdict(set, {"keyword": set(FULL)}))
    FAKE["ex"] = types.SimpleNamespace(sets=defaultdict(set, {"keyword": set(FULL), "full_text_norm": {"x"}}), manifest_sha256=PARENT)
    FAKE["union"] = {"exports": [union_ex]}
    Gf = fake_G(tmp_path)
    info = rg.require("A71", rg.KW_MARKER, PREREG)
    kn.install(Gf, info, root)
    kn.install(Gf, info, root)                                       # idempotent
    side = Gf.AcSide.load()
    assert side.ex.sets["keyword"] == set(KEEP) and union_ex.sets["keyword"] == set(KEEP)
    assert side.ex.sets["full_text_norm"] == {"x"}                   # every other kind is untouched
    rec = side.record()
    assert rec["manifest_verified"] and rec["keyword_narrow"]["ruling"]["id"] == "A71" and rec["keyword_narrow"]["narrowed_hashes"] == 2
    assert Gf.ac_guard_files()[-2:] == [root / "MANIFEST.json", root / "keyword_hashes.jsonl"]


def test_install_stops_the_run_on_any_problem_and_never_falls_back(tmp_path):
    FAKE["ex"] = types.SimpleNamespace(sets=defaultdict(set, {"keyword": set(FULL)}), manifest_sha256=PARENT)
    FAKE["union"] = None
    Gf = fake_G(tmp_path)
    kn.install(Gf, rg.require("A71", rg.KW_MARKER, PREREG), tmp_path / "missing_kw")
    with pytest.raises(kn.NarrowError):
        Gf.AcSide.load()
    assert FAKE["ex"].sets["keyword"] == FULL                         # nothing was swapped
    FAKE["ex"] = None                                                 # an export that did not verify: nothing to narrow, the run is incomplete anyway
    assert Gf.AcSide.load().ex is None


def test_the_real_export_dir_is_not_built_yet():
    assert not (C2B / kn.KW_DIR_NAME).exists()                        # option 2 (b) is a design: nothing was built or written


# ------------------------------------------------------------------------------------------------ frame text
FRAME_A = "Use the ledger rules to decide which payment arrives first."
FRAME_B = "Every hour on the hour the depot clerk logs the shipment status."
SHORT = "Pay the clerk first."
INSTANCE = "Mara owes Ivo forty coins from the spring market."


def make_family(tmp_path, with_pools=False):
    d = tmp_path / "blocks" / "T98"
    d.mkdir(parents=True)
    (d / "plugin.py").write_text(
        '"""Docstring that must never count as frame text because nobody renders it at all."""\n'
        f'CARD = "{FRAME_A}"\n'
        f'RULE = "{FRAME_B}\\n{{NAME}} signs the log."\n'
        f'SHORT = "{SHORT}"\n'
        'HELD_OUT_TOOLS = ["Quillmoor routing supervisor desk for the northern harbour"]\n'
        'def held_out_sampler():\n'
        '    return "A held out value sentence that is long enough to be a frame piece"\n')
    if with_pools:
        (d / "pools").mkdir()
        (d / "pools" / "skins.jsonl").write_text(json.dumps({"skin_id": "s1", "text": "Dear {NAME}, the pool wording with plenty of words follows."}) + "\n")
    return d


def test_held_out_lines_cover_assignments_and_functions():
    src = 'A = "x"\nHELD_OUT_X = [\n  "a",\n  "b"]\ndef held_out_f():\n    return "c"\ndef other():\n    return "d"\n'
    lines = fe.held_out_lines(src)
    assert lines == {2, 3, 4, 5, 6} and fe.held_out_lines("not python (") == set()


def test_build_index_takes_frame_pieces_from_code_only_and_never_held_out_values(tmp_path, monkeypatch):
    make_family(tmp_path, with_pools=True)
    monkeypatch.setattr(G, "block_dir", lambda b: tmp_path / "blocks" / b)
    idx = fe.build_index(G, ["T98"])
    p = idx.pieces["T98"]
    assert FRAME_A in p and FRAME_B in p                              # long enough, cut at the {NAME} placeholder
    assert not any("Docstring" in x or "Quillmoor" in x or "held out value" in x or x == SHORT for x in p), p
    assert not any("pool wording" in x for x in p)                    # scope code: pools are not frame
    idx2 = fe.build_index(G, ["T98"], "code+pools")
    assert any("pool wording" in x for x in idx2.pieces["T98"])
    with pytest.raises(SystemExit):
        fe.build_index(G, ["T98"], "everything")


def test_mask_is_token_exact_own_family_only_and_keeps_the_instance(tmp_path, monkeypatch):
    make_family(tmp_path)
    monkeypatch.setattr(G, "block_dir", lambda b: tmp_path / "blocks" / b)
    idx = fe.build_index(G, ["T98"])
    t = f"Note: use THE ledger rules to decide, which payment arrives first!  {INSTANCE}"
    out, n = idx.mask("T98", t)
    assert n == 1 and fe.SENTINEL in out and "ledger" not in out and INSTANCE in out and out.startswith("Note: ")
    assert idx.mask("T97", t) == (t, 0) and idx.mask(None, t) == (t, 0)           # another family's frame is not excused
    assert idx.mask("T98", "use the ledger rules to decide which payment arrives") == ("use the ledger rules to decide which payment arrives", 0)
    two, n2 = idx.mask("T98", FRAME_A + " " + FRAME_B)
    assert n2 == 2 and two == f"{fe.SENTINEL} {fe.SENTINEL}"
    assert idx.mask_obj("T98", {"k": [FRAME_A, 3, None]}) == {"k": [fe.SENTINEL, 3, None]}


class FakeSide:
    """Fake OHS-AC hash side: the frame sentence hits exact_sentence + ngram10; SEALEDSENT hits ngram10; ACKEY hits keyword; a text that is
    exactly the frame sentence also hits exact_full. Everything is complete."""

    def hash_compare(self, units):
        hits = {}
        for u in units:
            for _f, t in u["texts"]:
                low = t.lower()
                if "ledger rules to decide which payment arrives first" in low:
                    hits.setdefault("exact_sentence", {})[u["key"]] = {"state"}
                    hits.setdefault("ngram10", {})[u["key"]] = {"state"}
                if "SEALEDSENT" in t:
                    hits.setdefault("ngram10", {})[u["key"]] = {"state"}
                if "ACKEY" in t:
                    hits.setdefault("keyword", {})[u["key"]] = {"state"}
                if t.strip() in (FRAME_A, "Mara pays Ivo forty coins.", FRAME_A + " " + INSTANCE):
                    hits.setdefault("exact_full", {})[u["key"]] = {"state"}
        return hits, {}, {}

    def completeness(self, units, cover):
        return True, []

    def record(self):
        return {"manifest_verified": True, "final": True}


def fake_rc_factory(orig):
    def run_checker(tool, flag, records, extra=None, **kw):
        if tool in (G.G13_OHSAC_TOOL, G.GTPL_AC_TOOL):
            ids = [r["id"] for r in records if "ledger rules to decide which payment arrives first" in (r.get("state") or r.get("text") or "").lower()]
            return {"status": "scanned", "hit_ids": ids, "hit_ids_by_method": {"exact_seg": ids, "tulu8": ids}}
        return orig(tool, flag, records, extra, **kw)
    return run_checker


def mk_row(i, state, fam="T98", call=None, **kw):
    r = row(i, state, call=call, **kw)
    r["meta"] = {"family": fam}
    return r


@pytest.fixture()
def stage_world(tmp_path, monkeypatch):
    fam = make_family(tmp_path)
    monkeypatch.setattr(G, "block_dir", lambda b: tmp_path / "blocks" / b)
    monkeypatch.setattr(G, "run_checker", fake_rc_factory(G.run_checker))
    for n in ("ohsac_stage",):
        monkeypatch.setattr(G, n, getattr(G, n))
    monkeypatch.setattr(G, "_opt2_frame", False, raising=False)
    rows = [mk_row(0, FRAME_A + " Mara owes Ivo fifty coins from the autumn fair."),       # own frame + clean instance: excused
            mk_row(1, FRAME_A + " ACKEY " + INSTANCE),                 # own frame + keyword hit: keyword still binds
            mk_row(2, "Mara pays SEALEDSENT quickly. " + FRAME_A),     # own frame + instance-level n-gram: still hits
            mk_row(3, FRAME_A, call="c3", instructions=FRAME_B, card=FRAME_A),   # nothing but own frame in every field: pure frame, excused whole
            mk_row(4, FRAME_A + " " + INSTANCE, fam="T97"),            # the same words in another family's row: not excused
            mk_row(5, "A clean state about the canteen menu for next week and its prices."),
            mk_row(6, "Mara pays Ivo forty coins."),                   # a whole-text match with no frame in it: binds
            mk_row(7, FRAME_A + " " + INSTANCE)]                       # a whole-text match that CONTAINS frame + instance: exact_full binds
    units = G.row_units(rows)
    code, _ = G.code_seed_units("T98", fam)
    sets = {"c2_cand_T98": {"units": units, "code": code, "ac_code": [], "block": "T98"}}
    return {"sets": sets, "fam": fam}


def test_the_stage_without_the_option_is_unchanged(stage_world):
    res = G.ohsac_stage("candidates", stage_world["sets"], None, FakeSide())["c2_cand_T98"]
    assert {k for k in res["hash"]["exact_sentence"] if k.startswith("c")} == {"c0", "c1", "c2", "c3", "c4", "c7"}
    assert "frame_excuse" not in res["rec"] and any(k.startswith("seed:") for k in res["hash"]["exact_sentence"])      # the CARD literal hits too


def test_the_stage_excuses_only_own_frame_sentence_and_ngram_hits(stage_world):
    info = rg.require("A70", rg.FRAME_MARKER, PREREG)
    fe.install(G, info, "code")
    fe.install(G, info, "code")
    res = G.ohsac_stage("candidates", stage_world["sets"], None, FakeSide())["c2_cand_T98"]
    hit_units = {k for d in (res["hash"], res["rows"], res["gtpl"]) for m in d.values() for k in m}
    assert hit_units & {"c0", "c3", "c5"} == set()                     # excused (c0 frame + clean instance, c3 pure frame) / clean
    assert not any(k.startswith("seed:") for k in hit_units)           # the family's own CARD literal (pure frame) is excused too
    assert "c1" in res["hash"]["keyword"] and "c1" not in res["hash"].get("exact_sentence", {})
    assert "c2" in res["hash"]["ngram10"] and "c2" not in res["hash"].get("exact_sentence", {})   # instance-level n-gram still drops the unit
    assert {"c4"} <= set(res["hash"]["exact_sentence"]) and "c4" in res["rows"]["exact_seg"]   # another family's row is not excused
    assert "c6" in res["hash"]["exact_full"] and "c7" in res["hash"]["exact_full"]             # whole-text matches bind (c7 even with frame inside)
    assert "c7" not in res["hash"].get("exact_sentence", {}) and "c7" not in res["hash"].get("ngram10", {})
    assert "c0" not in res["rows"].get("exact_seg", {}) and "c0" not in res["rows"].get("tulu8", {})
    fx = res["rec"]["frame_excuse"]
    assert fx["ruling"]["id"] == "A70" and fx["scope"] == "code" and fx["pure_frame_units"] == 2
    assert fx["units_hit_unmasked"] == 8 and fx["units_hit_after"] == 5 and fx["units_excused"] == 3
    assert fx["excused_unit_method_pairs"]["ohsac_hash:exact_sentence"] == 6 and fx["excused_unit_method_pairs"]["ohsac_hash:exact_full"] == 2
    assert res["rec"]["complete"] is True and res["why"] == []
    assert "ledger" not in json.dumps(fx)                              # counts only


def test_the_program_literals_of_the_family_are_excused_but_a_literal_with_a_held_out_value_is_not(stage_world):
    """Seed-style units: a literal carrying the frame is masked (its own text); a held-out literal is never frame, so it is not masked."""
    idx = fe.build_index(G, ["T98"])
    sets = {"c2_cand_T98": {"units": [], "code": G.code_seed_units("T98", stage_world["fam"])[0], "ac_code": [], "block": "T98"}}
    m = fe.mask_sets(idx, sets)["c2_cand_T98"]["code"]
    texts = [t for u in m for _f, t in u["texts"]]
    assert any(t == fe.SENTINEL for t in texts)                       # CARD (a pure frame literal) is now only the sentinel
    assert any("Quillmoor routing supervisor" in t for t in texts) and any("held out value" in t for t in texts)


# ------------------------------------------------------------------------------------------------ the launcher
def test_launch_with_no_flag_runs_the_original(monkeypatch):
    seen = []
    monkeypatch.setattr(G, "main", lambda argv=None: seen.append(argv) or 0)
    for n in ("ohsac_stage", "derive_hits", "_record", "withdraw_waivers", "ac_guard_files"):
        monkeypatch.setattr(G, n, getattr(G, n))
    keep = (G.ohsac_stage, G.derive_hits, G.AcSide.load.__func__, G.ac_guard_files)
    assert launch.launch(["candidates", "--block", "T28"], PREREG) == 0
    assert seen == [["candidates", "--block", "T28"]]
    assert keep == (G.ohsac_stage, G.derive_hits, G.AcSide.load.__func__, G.ac_guard_files)


@pytest.mark.parametrize("argv, why", [
    (["--frame-excuse", "A99"], "no ruling block"),
    (["--frame-excuse", "A71"], "marker"),                              # a ruling for another option never arms this one
    (["--kw-narrow", "A70"], "marker"),
    (["--ohsac-report-only", "A70"], "marker"),
    (["--frame-excuse", "A70", "--frame-scope", "code+pools"], "OHSAC_FRAME_POOLS"),
    (["--frame-excuse", "A70", "--frame-scope", "all"], "--frame-scope must be"),
    (["--frame-scope", "code"], "needs --frame-excuse"),
    (["--kw-dir", "x"], "needs --kw-narrow")])
def test_launch_refuses_and_patches_nothing(monkeypatch, argv, why):
    seen = []
    monkeypatch.setattr(G, "main", lambda argv=None: seen.append(argv) or 0)
    for n in ("ohsac_stage", "derive_hits", "_record", "withdraw_waivers", "ac_guard_files"):
        monkeypatch.setattr(G, n, getattr(G, n))
    monkeypatch.setattr(G, "_opt2_frame", False, raising=False)
    monkeypatch.setattr(G, "_opt2_kw", False, raising=False)
    monkeypatch.setattr(G, "_opt3_capture", False, raising=False)
    before = (G.ohsac_stage, G.derive_hits, G.ac_guard_files)
    with pytest.raises(SystemExit) as e:
        launch.launch(["candidates"] + argv, PREREG)
    assert why in str(e.value) and seen == [] and before == (G.ohsac_stage, G.derive_hits, G.ac_guard_files)
    assert not (G._opt2_frame or G._opt2_kw or G._opt3_capture)


def test_launch_arms_each_option_separately(monkeypatch, tmp_path):
    seen = []
    monkeypatch.setattr(G, "main", lambda argv=None: seen.append(argv) or 0)
    for n in ("ohsac_stage", "derive_hits", "_record", "withdraw_waivers", "ac_guard_files"):
        monkeypatch.setattr(G, n, getattr(G, n))
    monkeypatch.setattr(G.AcSide, "load", G.AcSide.load)
    monkeypatch.setattr(G.AcSide, "record", G.AcSide.record)
    for f in ("_opt2_frame", "_opt2_kw", "_opt3_capture"):
        monkeypatch.setattr(G, f, False, raising=False)
    assert launch.launch(["candidates", "--frame-excuse", "A72", "--frame-scope", "code+pools", "--ohsac-report-only", "A73",
                          "--block", "T28"], PREREG) == 0
    assert seen == [["candidates", "--block", "T28"]] and G._opt2_frame is True and G._opt3_capture is True and not G._opt2_kw
    assert launch.launch(["candidates", "--kw-narrow", "A71", "--kw-dir", str(tmp_path / "kw")], PREREG) == 0
    assert G._opt2_kw is True


def test_no_id_arms_option_2_in_the_real_prereg():
    """Only the A68 machine marker (option 3, owner ruling 17 Oct) is in PREREG_FINAL.md: no id arms option 2 (a) or (b)."""
    text = Path(c2io.PREREG).read_text(encoding="utf-8")
    for marker in (rg.FRAME_MARKER, rg.KW_MARKER, fe.POOLS_MARKER):
        assert marker not in text
    for rid in rg.ruling_blocks(text):
        for marker in (rg.FRAME_MARKER, rg.KW_MARKER):
            assert rg.check(rid, marker, text)[0] is None


def test_the_pinned_tools_are_not_edited_by_option_2():
    for n in ("g13_c2.py", "mix_c2.py", "c2_select.py"):
        src = (C2B / n).read_text(encoding="utf-8")
        assert "frame_excuse" not in src and "keyword_narrow" not in src
