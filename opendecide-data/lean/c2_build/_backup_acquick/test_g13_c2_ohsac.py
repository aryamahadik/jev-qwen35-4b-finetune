"""Tests for the OHS-AC path of g13_c2.py and the computed `complete` of zed_orch/a57_hashcheck_ac.py / a57_hashcmp.py (Ruling A64 (g)).
Synthetic data only: a synthetic OHS-AC hash export (built here in the MANIFEST layout of sealed_hashes_ac from a few synthetic texts), a
synthetic union record, a synthetic PREREG addendum with synthetic finality shas, and two FAKE sealed-side checkers (so no real sealed checker or
export is run or read). No "ohs" path is opened. Run from lean/:
  ../.venv/bin/python -m pytest -q c2_build/tests/test_g13_c2_ohsac.py
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
import textwrap
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(C2B / "zed_orch"))
import c2io  # noqa: E402
import g13_c2 as G  # noqa: E402
from test_g13_c2 import (A38, EVAL_SENT, SUITE_HOST, SUITE_KEYWORD, SUITE_LONG, exports, fake_tools, make_exports, row,  # noqa: E402,F401
                         world)

g = G.g
A42D = "a" * 64
SUITE_SHA, POST_SHA, SRC_SHA = "b" * 64, "c" * 64, "5" * 64
FREEZE_EXPORT = "27808b0c" + "e" * 56
RAW_ONLY = "Alpha beta gamma delta epsilon zeta."         # in the export's full_text_raw ONLY: nothing else finds it
UNION_ONLY = "Union only wording that sits in the extra union files and nowhere else at all."
ACLEAK, ACTPL = "ACLEAK", "ACTPL"


# ------------------------------------------------------------------------------------------------ a synthetic OHS-AC export
def _records(root: Path) -> dict:
    import numpy as np
    rec = {}
    for n in (10, 12):
        rec[f"ngrams{n}_sha256.npy"] = int(len(np.load(root / f"ngrams{n}_sha256.npy")))
    for f in ("text_hashes.jsonl", "structure_hashes.jsonl", "keyword_hashes.jsonl"):
        per: dict = {}
        for ln in (root / f).read_text().splitlines():
            if ln.strip():
                k = json.loads(ln)["kind"]
                per.setdefault(k, set()).add(json.loads(ln)["hash"])
        rec[f] = {k: len(v) for k, v in per.items()}
    return rec


def _shas(root: Path) -> dict:
    return {n: G._sha_file(root / n) for n in G.AC_FILES}


def build_ac(root: Path, *, stage: str = "post_freeze", suite_sha: str = SUITE_SHA, raw_only: bool = True) -> dict:
    """Write a synthetic OHS-AC export folder at `root` (MANIFEST layout of sealed_hashes_ac). Returns the shas the addendum must name."""
    make_exports(root)                                                    # the files (the OHS-4 layout MANIFEST is replaced below)
    if raw_only:
        with open(root / "text_hashes.jsonl", "a") as f:
            f.write(json.dumps({"kind": "full_text_raw", "hash": G.sha_hex(RAW_ONLY)}) + "\n")
    (root / "FORMAT.md").write_text("synthetic format notes\n")
    man = {"a42d_block_sha256": A42D, "calls": 3, "final_suite_sha256": suite_sha, "format_md_sha256": G._sha_file(root / "FORMAT.md"),
           "frozen_suite_sha256": "9" * 64, "post_freeze_manifest_sha256": POST_SHA, "records": _records(root),
           "sha256": _shas(root), "source_manifest_sha256": SRC_SHA, "stage": stage, "suite": "OHS-AC"}
    (root / "MANIFEST.json").write_text(json.dumps(man))
    return {"manifest": G._sha_file(root / "MANIFEST.json"), "final_suite": SUITE_SHA, "post_freeze": POST_SHA, "source": SRC_SHA}


def prereg_for(shas: dict) -> str:
    return (A38 + f"\n> A42-D block sha256 `{A42D}`.\n\n"
            "> **Post-freeze addendum (A57 step 5; synthetic).** Final suite\n"
            f"> sha256 `{shas['final_suite']}`; POST_FREEZE manifest sha256\n"
            f"> `{shas['post_freeze']}`; hash-only re-export MANIFEST sha256\n"
            f"> `{shas['manifest']}` (the union of this export and the freeze export\n"
            "> `27808b0c…` binds every later G13 / admission check). **3 items** = the frozen items (MANIFEST `"
            f"{shas['source'][:8]}…`,\n> verified unchanged).\n\nThe freeze manifest was `{shas['source']}`.\n")


def write_union(root: Path, ac_root: Path, status: str = "freeze_subset_of_final", count: int = 0, freeze: str = FREEZE_EXPORT,
                with_files: bool = False) -> None:
    root.mkdir(parents=True, exist_ok=True)
    man = json.loads((ac_root / "MANIFEST.json").read_text())
    counts = {n: count for n, v in man["records"].items() if not isinstance(v, dict)}
    counts.update({f"{f}:{k}": count for f, d in man["records"].items() if isinstance(d, dict) for k in d})
    rec = {"status": status, "freeze_manifest_sha256": freeze, "final_manifest_sha256": G._sha_file(ac_root / "MANIFEST.json"),
           "counts_per_kind_freeze_minus_final": counts}
    if with_files:
        for n in G.AC_FILES:
            shutil.copy(ac_root / n, root / n)
        with open(root / "text_hashes.jsonl", "a") as f:
            f.write(json.dumps({"kind": "full_text_raw", "hash": G.sha_hex(UNION_ONLY)}) + "\n")
        rec["sha256"], rec["records"] = _shas(root), _records(root)
    (root / "RECORD.json").write_text(json.dumps(rec))


@pytest.fixture()
def ac(tmp_path, monkeypatch):
    """A synthetic OHS-AC world: final export + addendum + freeze_subset_of_final record, wired into g13_c2 (module paths) and c2io.PREREG."""
    root, union = tmp_path / "ac", tmp_path / "ac_union"
    shas = build_ac(root)
    write_union(union, root)
    text = prereg_for(shas)
    pre = tmp_path / "PREREG.md"
    pre.write_text(text)
    monkeypatch.setattr(G, "EXPORTS_AC", root)
    monkeypatch.setattr(G, "EXPORTS_AC_UNION", union)
    monkeypatch.setattr(G, "AC_A42D_SHA256", A42D)
    monkeypatch.setattr(c2io, "PREREG", pre)
    return {"root": root, "union": union, "shas": shas, "prereg": text, "path": pre}


def side(ac_) -> "G.AcSide":
    return G.AcSide.load(prereg_text=ac_["prereg"])


# ------------------------------------------------------------------------------------------------ the finality / union rules
def test_a_final_export_with_a_union_record_is_complete(ac):
    s = side(ac)
    assert s.ex is not None and s.ex.finality["ok"] and s.union["ok"] and not s.problems
    assert s.ex.stage == "post_freeze"                                    # the stage string is recorded; it decides nothing
    units = G.ac_units([{"key": "u", "texts": [("state", "A clean synthetic sentence about canteen menus next week.")], "rows_src": [
        {"state": "A clean synthetic sentence about canteen menus next week.", "instructions": "Answer."}]}])
    hits, _rep, cover = s.hash_compare(units)
    assert hits == {} and s.completeness(units, cover) == (True, [])


def test_a_known_hit_is_found_and_stays_a_hit(ac):
    s = side(ac)
    row_u = {"key": "c1", "texts": [("state", "Log entry follows. " + SUITE_LONG + " End.")],
             "rows_src": [{"state": "Log entry follows. " + SUITE_LONG + " End.", "instructions": "Answer the question."}]}
    hits, _rep, cover = s.hash_compare(G.ac_units([row_u]))
    assert {"ngram10", "ngram12", "exact_sentence"} <= set(hits) and all("c1" in v for v in hits.values())
    assert s.completeness(G.ac_units([row_u]), cover)[0]                  # complete AND a hit: the hit decides, not the completeness


def test_stage_string_decides_nothing_the_addendum_shas_do(tmp_path, monkeypatch):
    monkeypatch.setattr(G, "AC_A42D_SHA256", A42D)
    # stage says "final" but the suite sha is not the addendum's: not final
    root = tmp_path / "ac"
    shas = build_ac(root, stage="final", suite_sha="d" * 64)
    write_union(tmp_path / "u", root)
    s = G.AcSide.load(root, tmp_path / "u", prereg_text=prereg_for(shas))
    assert s.ex.stage == "final" and not s.ex.is_final and s.ex.finality["checks"]["final_suite"] is False
    assert not s.completeness([], {})[0] and any("final_suite" in w for w in s.problems)
    # stage says "post_freeze" (the real export's string) and the shas are the addendum's: final
    root2 = tmp_path / "ac2"
    shas2 = build_ac(root2, stage="post_freeze")
    write_union(tmp_path / "u2", root2)
    s2 = G.AcSide.load(root2, tmp_path / "u2", prereg_text=prereg_for(shas2))
    assert s2.ex.is_final and s2.completeness([], {})[0]


def test_each_addendum_sha_binds(ac, tmp_path):
    for k in ("manifest", "final_suite", "post_freeze", "source"):
        shas = dict(ac["shas"])
        shas[k] = "e" * 64 if k != "source" else "6" * 64
        s = G.AcSide.load(ac["root"], ac["union"], prereg_text=prereg_for(shas))
        assert s.ex is not None and not s.ex.finality["checks"][k] and not s.completeness([], {})[0], k


def test_no_addendum_in_the_prereg_means_not_final(ac):
    s = G.AcSide.load(prereg_text=A38 + f"\n> A42-D block sha256 `{A42D}`.\n")
    assert s.ex is not None and not s.ex.is_final and any("addendum" in w for w in s.problems)


def test_a_missing_union_record_is_not_complete(ac):
    (ac["union"] / "RECORD.json").unlink()
    s = side(ac)
    assert s.union["status"] == "missing" and not s.union["ok"]
    assert not s.completeness([], {})[0] and any("union record" in w for w in s.problems)


@pytest.mark.parametrize("mutate", ["lost", "bad_status", "nonzero", "wrong_freeze", "other_final", "unreadable", "no_counts"])
def test_a_bad_union_record_is_not_complete(ac, mutate):
    p = ac["union"] / "RECORD.json"
    d = json.loads(p.read_text())
    if mutate == "lost":
        d["status"] = "lost"
    elif mutate == "bad_status":
        d["status"] = "fine"
    elif mutate == "nonzero":
        d["counts_per_kind_freeze_minus_final"]["keyword_hashes.jsonl:keyword"] = 3
    elif mutate == "wrong_freeze":
        d["freeze_manifest_sha256"] = "0" * 64
    elif mutate == "other_final":
        d["final_manifest_sha256"] = "1" * 64
    elif mutate == "no_counts":
        del d["counts_per_kind_freeze_minus_final"]
    if mutate == "unreadable":
        p.write_text("{not json")
    else:
        p.write_text(json.dumps(d))
    s = side(ac)
    assert not s.union["ok"] and not s.completeness([], {})[0]


def test_a_union_built_record_adds_its_files_to_the_compare(ac):
    write_union(ac["union"], ac["root"], status="union_built", count=1, with_files=True)
    s = side(ac)
    assert s.union["ok"] and len(s.union["exports"]) == 1 and s.completeness([], {})[0]
    u = G.ac_unit_from_texts("t", [("text", UNION_ONLY)], True)
    hits, _r, cover = s.hash_compare([u])
    assert "exact_raw" in hits and "t" in hits["exact_raw"] and s.completeness([u], cover)[0]
    # the file shas of the union files bind
    with open(ac["union"] / "keyword_hashes.jsonl", "a") as f:
        f.write(json.dumps({"kind": "keyword", "hash": "0" * 64}) + "\n")
    s2 = side(ac)
    assert not s2.union["ok"] and not s2.completeness([], {})[0]
    # union_built without files / shas is not ok
    d = json.loads((ac["union"] / "RECORD.json").read_text())
    del d["sha256"]
    (ac["union"] / "RECORD.json").write_text(json.dumps(d))
    assert not side(ac).union["ok"]


def test_a_tampered_export_does_not_verify(ac):
    with open(ac["root"] / "keyword_hashes.jsonl", "a") as f:
        f.write(json.dumps({"kind": "keyword", "hash": "0" * 64}) + "\n")
    s = side(ac)
    assert s.ex is None and s.manifest_error and not s.completeness([], {})[0]
    assert s.record()["manifest_verified"] is False


# ------------------------------------------------------------------------------------------------ the units
def test_a_template_unit_still_runs_exact_raw(ac):
    s = side(ac)
    u = G.ac_unit_from_texts("tpl", [("pool", RAW_ONLY)], True)
    hits, _r, cover = s.hash_compare([u])
    assert set(hits) == {"exact_raw"} and "tpl" in hits["exact_raw"]       # nothing else matches: only the raw compare finds it
    assert cover["tpl"] == set(G.AC_REQUIRED_METHODS)
    # the old way (a cut template, no uncut pass, no rows_src) never runs exact_raw and leaves methods unrun
    old = {"key": "tpl", "texts": [("pool", RAW_ONLY)], "template": True}
    h2, _r2, c2 = s.hash_compare([old])
    assert h2 == {} and "exact_raw" not in c2["tpl"] and not s.completeness([old], c2)[0]


def test_every_required_method_must_have_run_on_every_unit(ac):
    s = side(ac)
    ok = G.ac_unit_from_texts("a", [("pool", "Some synthetic template text for {NAME} with enough words in it.")], True)
    bare = {"key": "b", "texts": [("text", "A bare unit with enough words to be compared but no rows.")], "template": False}
    _h, _r, cover = s.hash_compare([ok, bare])
    assert cover["a"] == set(G.AC_REQUIRED_METHODS) and "structure_g13" not in cover["b"]
    done, why = s.completeness([ok, bare], cover)
    assert not done and any("1 unit(s) did not get every required method" in w for w in why)


def test_held_out_token_fixture(ac):
    s = side(ac)
    tpl = G.ac_unit_from_texts("kw", [("pool", "Ship {N} units with " + SUITE_KEYWORD + " by Friday please.")], True)
    url = G.ac_unit_from_texts("host", [("pool", f"Track it at https://www.{SUITE_HOST}/track today, {{NAME}}.")], True)
    clean = G.ac_unit_from_texts("clean", [("pool", "Ship {N} units with the regular carrier by Friday please.")], True)
    hits, _r, _c = s.hash_compare([tpl, url, clean])
    assert set(hits["keyword"]) == {"kw", "host"}
    assert not any("clean" in v for v in hits.values())


def test_program_units_keep_their_rows_and_templates_are_cut_and_uncut():
    rows = [{"id": "r1", "state": "State one of the unit with several words.", "instructions": "Do it now please.", "options": ["a", "b"]}]
    row_unit = {"key": "c1", "rows": ["r1"], "texts": [("state", rows[0]["state"])], "rows_src": rows, "template": False}
    tpl = {"key": "p", "texts": [("pool", "Text {X} here")], "template": True}
    out = {u["key"]: u for u in G.ac_units([row_unit, tpl, {"key": "empty", "texts": [], "rows_src": []}])}
    assert set(out) == {"c1", "p"} and out["c1"]["rows_src"] is rows and not out["c1"].get("uncut_too")
    assert out["p"]["uncut_too"] and out["p"]["rows_src"] == [{"state": "Text {X} here", "instructions": "Text {X} here"}]


def test_old_target_hash_hits_unchanged_by_the_new_args(exports):
    """ohs4_hash_hits(units, ex) with no cover and no uncut_too is the predecessor's function, field for field."""
    spec = importlib.util.spec_from_file_location("g13_pred", C2B / "_backup_refresh" / "g13_c2.py")
    pred = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pred)
    units = [{"key": "a", "texts": [("state", "Log entry follows. " + SUITE_LONG), ("option", "Not yet due")], "template": False,
              "rows_src": [{"state": "Log entry follows. " + SUITE_LONG, "options": ["Not yet due"]}]},
             {"key": "b", "texts": [("pool", "Dear {NAME}, " + SUITE_LONG)], "template": True},
             {"key": "c", "texts": [("pool", f"Ship {SUITE_KEYWORD} {{N}}")], "template": True}]
    assert G.ohs4_hash_hits(units, exports) == pred.ohs4_hash_hits(units, exports)


# ------------------------------------------------------------------------------------------------ the g13_c2 run
FAKE_AC_ROWS = textwrap.dedent('''\
    import json, sys
    a = sys.argv
    inp, out = a[a.index("--rows") + 1], a[a.index("--out") + 1]
    rows = [json.loads(x) for x in open(inp) if x.strip()]
    unit = {}
    for r in rows:
        unit.setdefault(r.get("call_id") or r["id"], []).append(r["id"])
    hit_units = {r.get("call_id") or r["id"] for r in rows if "ACLEAK" in json.dumps(r)}
    ids = sorted(i for u in hit_units for i in unit[u])
    d = {"tool": "g13_ohsac_check", "version": 1, "suite": "OHS-AC", "manifest_verified": True, "suite_sha256": "5" * 64,
         "g13_sha256": "0" * 64, "input_sha256": "1" * 64, "params": {}, "methods": ["exact_seg"],
         "counts": {"c2_rows": len(rows), "hit_rows": len(ids)}, "hit_ids": ids, "hit_ids_by_method": {"exact_seg": ids},
         "complete": True, "wall_s": 0.0}
    open(out, "w").write(json.dumps(d))
    sys.exit(4 if ids else 0)
    ''')
FAKE_AC_GTPL = textwrap.dedent('''\
    import json, sys
    a = sys.argv
    assert a[a.index("--min-shared") + 1] == "1" and a[a.index("--parts") + 1] == "all", a
    inp, out = a[a.index("--templates") + 1], a[a.index("--out") + 1]
    ts = [json.loads(x) for x in open(inp) if x.strip()]
    ids = sorted(t["id"] for t in ts if "ACTPL" in t["text"])
    d = {"tool": "gtpl_check_ac", "version": 1, "suite": "OHS-AC", "manifest_verified": True, "suite_sha256": "5" * 64,
         "g13_sha256": "0" * 64, "input_sha256": "1" * 64, "ngram": 8, "scope_parts": ["R", "U"],
         "counts": {"templates": len(ts), "hit_templates": len(ids)}, "hit_ids": ids, "complete": True, "wall_s": 0.0}
    open(out, "w").write(json.dumps(d))
    sys.exit(4 if ids else 0)
    ''')


@pytest.fixture()
def acw(world, ac, tmp_path, monkeypatch):
    """The end-to-end world of test_g13_c2 with an OHS-AC export, a union record and fake OHS-AC checkers."""
    d = tmp_path / "fake_ac_tools"
    d.mkdir()
    (d / "rows.py").write_text(FAKE_AC_ROWS)
    (d / "gtpl.py").write_text(FAKE_AC_GTPL)
    monkeypatch.setattr(G, "G13_OHSAC_TOOL", d / "rows.py")
    monkeypatch.setattr(G, "GTPL_AC_TOOL", d / "gtpl.py")
    crow = [row(0, "Clean state about the canteen menu for next week and its prices."),
            row(1, "Log entry follows. " + SUITE_LONG + " End of log."),
            row(2, "A row carrying ACLEAK text in its state for the fake AC checker, nothing more."),
            row(3, "Another clean row about the library opening hours during the spring term.")]
    world["cand"].write_text("".join(json.dumps(r) + "\n" for r in crow))
    recs = [{"skin_id": "clean", "text": "Hi {NAME}, the parcel for {ITEM} left the depot this morning."},
            {"skin_id": "hashhit", "text": "Dear {NAME}, " + SUITE_LONG},
            {"skin_id": "rawonly", "text": RAW_ONLY},
            {"skin_id": "kwhit", "text": "Ship {N} units with " + SUITE_KEYWORD + " by Friday please."},
            {"skin_id": "acleak", "text": "An ACLEAK line for {NAME} and more words follow here."},
            {"skin_id": "actpl", "text": "ACTPL wording for {NAME} with enough words to count."}]
    (world["pools"] / "skins.jsonl").write_text("".join(json.dumps(r) + "\n" for r in recs))
    world["plugin"].write_text('CARD = "Use the ledger rules to decide which payment arrives first."\n'
                               'TPL = "ACTPL program sentence with several more words in it."\n'
                               'LIT = "Program literal. ' + SUITE_LONG + '"\n')
    return {**world, **{"ac": ac}}


def run_ac(w, run_name, **kw):
    tgs = w["tgs"] + (G.c2_dev_targets() if run_name == "candidates" else [])
    return G.run(run_name, ["T98"], embed=False, side=False, tgs=tgs, exports=w["exports"], write=False,
                 prereg_text=w["ac"]["prereg"], ohsac=True, **kw)


def test_candidates_run_drops_ac_hits_and_records_the_stage(acw):
    rec = run_ac(acw, "candidates")["c2_cand_T98"]
    oa = rec["ohsac"]
    assert oa["manifest_verified"] and oa["final"] and oa["union"]["status"] == "freeze_subset_of_final" and oa["complete"]
    assert not any(w.startswith("ohsac") for w in rec["incomplete_why"])
    assert {"r1", "r2"} <= set(rec["drop_ids"]) and not {"r0", "r3"} & set(rec["drop_ids"])
    by = rec["counts_by_target_and_method"]
    assert by["ohsac_hash"] and by["ohsac_rows"]["exact_seg"]["units"] == 1
    assert oa["hit_ids"] == ["c1", "c2"] and oa["hit_units"] == 2
    assert oa["counts_by_method"]["ohsac_rows"] == by["ohsac_rows"] and oa["units_missing_methods"] == 0
    assert oa["gtpl_args"] == ["--min-shared", "1", "--parts", "all"] and oa["rows_checker"]["status"] == "scanned"
    assert "waivers" in oa and set(G.AC_TARGETS).isdisjoint(G.A53_TARGETS)       # A53 never touches an OHS-AC target
    # the program literal that carries a suite sentence and the ACTPL literal are listed (G-TPL via the fake AC checker)
    assert len(oa["program_literal_hits"]) == 2
    json.dumps(rec)


def test_seed_run_quarantines_templates_and_program_literals(acw):
    rec = run_ac(acw, "seed")["c2_seed_T98"]
    q = {x["template_id"]: x["hits"] for x in rec["quarantine"] if x["template_id"] in
         {"clean", "hashhit", "rawonly", "kwhit", "acleak", "actpl"}}
    assert set(q) == {"hashhit", "rawonly", "kwhit", "acleak", "actpl"}, q
    assert set(q["hashhit"]) >= {"ohsac_hash"} and set(q["rawonly"]) == {"ohsac_hash"}
    assert set(q["acleak"]) == {"ohsac_rows"} and set(q["actpl"]) == {"ohsac_gtpl"}
    assert "exact_raw" in rec["counts_by_target_and_method"]["ohsac_hash"]        # the template unit's raw compare ran
    lit = [x for x in rec["quarantine"] if x["template_id"].endswith(("#1", "#2"))]
    assert len(lit) == 2 and rec["drop_ids"] == []                                 # the program literals are quarantined too
    assert rec["ohsac"]["complete"] and rec["quarantine_templates"] == 7


def test_a_non_final_or_unioned_less_run_is_incomplete_but_keeps_its_drops(acw):
    (acw["ac"]["union"] / "RECORD.json").unlink()
    rec = run_ac(acw, "candidates")["c2_cand_T98"]
    assert not rec["ohsac"]["complete"] and any(w.startswith("ohsac: union record") for w in rec["incomplete_why"])
    assert not rec["complete"] and {"r1", "r2"} <= set(rec["drop_ids"])            # incomplete does not lose the drops


def test_a_checker_failure_makes_the_log_incomplete(acw, tmp_path, monkeypatch):
    bad = tmp_path / "bad.py"
    bad.write_text("import sys, json; print(json.dumps({'error': 'input'})); sys.exit(2)\n")
    monkeypatch.setattr(G, "G13_OHSAC_TOOL", bad)
    rec = run_ac(acw, "candidates")["c2_cand_T98"]
    assert not rec["ohsac"]["complete"] and any("ohsac_rows" in w for w in rec["incomplete_why"])


def test_the_export_files_and_both_checker_paths_are_in_the_run_guard(acw):
    files = G.ac_guard_files()
    assert G.G13_OHSAC_TOOL in files and G.GTPL_AC_TOOL in files
    assert {"MANIFEST.json", "FORMAT.md", "RECORD.json", *G.AC_FILES} <= {Path(p).name for p in files}
    sets = G.build_sets("candidates", ["T98"], G.LinkGuardedInputLog())
    on = G.run_guard("candidates", sets, ohsac=True).inputs_at_start()
    off = G.run_guard("candidates", sets).inputs_at_start()
    assert {"text_hashes.jsonl", "ngrams10_sha256.npy", "RECORD.json"} <= set(on) and "text_hashes.jsonl" not in off
    # a changed export file during a run is seen like any other input
    g_ = G.run_guard("candidates", sets, ohsac=True)
    with open(acw["ac"]["root"] / "keyword_hashes.jsonl", "a") as f:
        f.write("\n")
    assert any("keyword_hashes.jsonl" in w for w in g_.check())


def test_the_real_sealed_checkers_are_listed_in_the_guard_but_never_hashed(monkeypatch):
    monkeypatch.undo()                                                   # the real tool constants, not a fixture's fake paths
    real = [G.LEAN / "ohs_ac_sealed" / "tools" / n for n in ("g13_ohsac_check.py", "gtpl_check_ac.py")]
    assert G.G13_OHSAC_TOOL == real[0] and G.GTPL_AC_TOOL == real[1] and real[0] in G.ac_guard_files() and real[1] in G.ac_guard_files()
    touched = []
    monkeypatch.setattr(G.g, "sha256_file", lambda p: touched.append(str(p)) or "x")
    monkeypatch.setattr(G, "_sha_file", lambda p: touched.append(str(p)) or "x")
    guard = G.RunGuard(lambda: [(p, G.ALL, None) for p in real])
    assert guard.start == {} and guard.check() == [] and not touched    # the never-open rule drops them before any stat or hash
    assert c2io.refusal(G.AC_SEALED_TOOLS) and c2io.refusal(real[0]) and c2io.refusal(real[1])


def test_the_real_checker_paths_are_never_opened_by_the_source():
    import re
    src = Path(G.__file__).read_text()
    assert not re.search(r"(open|read_text|read_bytes|sha256_file|_sha_file|rglob|iterdir|glob)\([^)]*(AC_SEALED_TOOLS|G13_OHSAC_TOOL|GTPL_AC_TOOL)", src)
    assert c2io.refusal(G.G13_OHSAC_TOOL) and c2io.refusal(G.GTPL_AC_TOOL)


def test_status_flags_a_log_with_no_complete_ac_record(acw, tmp_path, monkeypatch):
    monkeypatch.setattr(G, "OHSAC_ON", True)
    rec = run_ac(acw, "candidates")["c2_cand_T98"]
    f = tmp_path / "c2_cand_T98.json"
    f.write_text(json.dumps(rec))
    assert not any("OHS-AC" in p for p in G.log_problems([f]))
    d = dict(rec)
    d.pop("ohsac")
    f.write_text(json.dumps(d))
    assert any("no OHS-AC record" in p for p in G.log_problems([f]))
    d["ohsac"] = {**rec["ohsac"], "complete": False}
    f.write_text(json.dumps(d))
    assert any("OHS-AC record is not complete" in p for p in G.log_problems([f]))


# ------------------------------------------------------------------------------------------------ the two zed_orch tools
def _load_tool(name: str):
    spec = importlib.util.spec_from_file_location(name, C2B / "zed_orch" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _units_file(tmp_path, texts: dict) -> Path:
    p = tmp_path / "u.jsonl"
    p.write_text("".join(json.dumps({"id": k, "text": v}) + "\n" for k, v in texts.items()))
    return p


CLEAN = "A clean synthetic sentence about canteen menus next week and its prices."


def test_hashcheck_tool_computes_complete_and_exit_codes(ac, tmp_path, capsys):
    HC = _load_tool("a57_hashcheck_ac")
    out = tmp_path / "r.json"
    f = _units_file(tmp_path, {"clean": CLEAN})
    assert HC.main(["texts", str(f), "--out", str(out)]) == 0
    r = json.loads(out.read_text())
    assert r["complete"] is True and r["manifest_verified"] and r["final"] and r["union"]["ok"] and r["counts"]["hit_units"] == 0
    f = _units_file(tmp_path, {"clean": CLEAN, "hit": "Log entry follows. " + SUITE_LONG, "raw": RAW_ONLY})
    assert HC.main(["texts", str(f), "--out", str(out)]) == 4                    # complete, with hits
    r = json.loads(out.read_text())
    assert r["complete"] and set(r["hit_ids"]) == {"hit", "raw"} and "exact_raw" in r["counts"]["by_method"]
    (ac["union"] / "RECORD.json").unlink()                                       # no union record: not complete, exit 3, hits still listed
    assert HC.main(["texts", str(f), "--out", str(out)]) == 3
    r = json.loads(out.read_text())
    assert r["complete"] is False and set(r["hit_ids"]) == {"hit", "raw"} and any("union record" in w for w in r["incomplete_why"])


def test_hashcheck_tool_non_final_export_is_never_complete(tmp_path, monkeypatch):
    HC = _load_tool("a57_hashcheck_ac")
    root = tmp_path / "ac"
    shas = build_ac(root, stage="final", suite_sha="d" * 64)                   # the stage string says final; the suite sha is not the addendum's
    write_union(tmp_path / "u", root)
    pre = tmp_path / "PREREG.md"
    pre.write_text(prereg_for(shas))
    monkeypatch.setattr(G, "EXPORTS_AC", root)
    monkeypatch.setattr(G, "EXPORTS_AC_UNION", tmp_path / "u")
    monkeypatch.setattr(c2io, "PREREG", pre)
    monkeypatch.setattr(G, "AC_A42D_SHA256", A42D)
    f = _units_file(tmp_path, {"clean": CLEAN})
    assert HC.main(["texts", str(f), "--out", str(tmp_path / "r.json")]) == 3
    r = json.loads((tmp_path / "r.json").read_text())
    assert r["complete"] is False and r["final"] is False and r["stage_string_recorded_only"] == "final"


def test_hashcheck_tool_refuses_an_export_that_does_not_verify(ac, tmp_path, capsys):
    HC = _load_tool("a57_hashcheck_ac")
    (ac["root"] / "FORMAT.md").write_text("changed\n")
    assert HC.main(["texts", str(_units_file(tmp_path, {"c": CLEAN})), "--out", str(tmp_path / "r.json")]) == 2
    assert not (tmp_path / "r.json").exists()


def test_hashcheck_tool_legacy_callers_get_every_method_and_the_old_keys(ac):
    """The A57 drivers build units by hand ({key, texts, template}) and call HC.run(units, ex): run() rebuilds them through ac_unit_from_texts so
    every required method is set up, and keeps the legacy output keys export_stage / export_final / final_suite_sha256 (export_final is COMPUTED)."""
    HC = _load_tool("a57_hashcheck_ac")
    ex = HC.ExportsAC()
    for tpl in (True, False):
        r = HC.run([{"key": "t", "texts": [("text", CLEAN)], "template": tpl}], ex)
        assert r["complete"] is True and r["counts"]["units_missing_methods"] == 0
        assert r["export_final"] is True and r["export_final"] == r["final"] and r["export_stage"] == r["stage_string_recorded_only"]
        assert r["final_suite_sha256"] and r["manifest_verified"] and r["manifest_sha256"]
    hit = HC.run([{"key": "h", "texts": [("text", "Log entry follows. " + SUITE_LONG)], "template": True}], ex)
    assert hit["hit_ids"] == ["h"]
    assert HC.run([HC.G.ac_unit_from_texts("t", [("text", CLEAN)], True)], ex)["complete"] is True


def test_hashcheck_tool_legacy_export_final_is_computed_not_the_stage_string(tmp_path, monkeypatch):
    HC = _load_tool("a57_hashcheck_ac")
    root = tmp_path / "ac"
    shas = build_ac(root, stage="final", suite_sha="d" * 64)
    write_union(tmp_path / "u", root)
    pre = tmp_path / "PREREG.md"
    pre.write_text(prereg_for(shas))
    monkeypatch.setattr(G, "EXPORTS_AC", root)
    monkeypatch.setattr(G, "EXPORTS_AC_UNION", tmp_path / "u")
    monkeypatch.setattr(c2io, "PREREG", pre)
    monkeypatch.setattr(G, "AC_A42D_SHA256", A42D)
    r = HC.run([{"key": "t", "texts": [("text", CLEAN)], "template": False}], HC.ExportsAC())
    assert r["export_stage"] == "final" and r["export_final"] is False and r["complete"] is False


def test_hashcmp_tool_computed_complete(ac, tmp_path, monkeypatch, exports):
    HM = _load_tool("a57_hashcmp")
    out = tmp_path / "r.json"
    f = _units_file(tmp_path, {"clean": CLEAN, "raw": RAW_ONLY})
    assert HM.main(["--export", "ac", "--units", str(f), "--out", str(out)]) == 4
    r = json.loads(out.read_text())
    assert r["complete"] and r["hit_ids"] == ["raw"] and r["by_method"] == {"exact_raw": 1} and r["final"]
    (ac["union"] / "RECORD.json").write_text(json.dumps({"status": "lost"}))
    assert HM.main(["--export", "ac", "--units", str(f), "--out", str(out)]) == 3
    assert json.loads(out.read_text())["complete"] is False
    monkeypatch.setattr(HM.G, "Exports", lambda: exports)                       # the OHS-4 branch, on the synthetic OHS-4 export
    f2 = _units_file(tmp_path, {"clean": CLEAN, "hit": "Dear {NAME}, " + SUITE_LONG})
    assert HM.main(["--export", "ohs4", "--units", str(f2), "--out", str(out)]) == 4
    r = json.loads(out.read_text())
    assert r["complete"] is True and r["hit_ids"] == ["hit"] and r["union"] == "n/a"


# ------------------------------------------------------------------------------------------------ the OHS-AC-only run
def test_ac_only_run_gives_the_same_drops_as_the_full_run_and_is_not_a_g13_log(acw):
    full = run_ac(acw, "candidates")["c2_cand_T98"]
    only = G.run_ohsac_only("candidates", ["T98"], write=True, prereg_text=acw["ac"]["prereg"])["c2_cand_T98"]
    assert only["mode"] == "ohsac_only" and only["complete"] is False and only["ohsac_complete"] is True
    assert set(only["drop_ids"]) == {"r1", "r2"} and only["drop_ids"] == sorted(set(full["drop_ids"]) & set(only["drop_ids"]))
    assert {k: v for k, v in only["counts_by_target_and_method"].items()} == \
        {k: v for k, v in full["counts_by_target_and_method"].items() if k.startswith("ohsac_")}
    assert only["ohsac"]["hit_ids"] == full["ohsac"]["hit_ids"] == ["c1", "c2"]
    paths = list(acw["writes"])
    assert len(paths) == 1 and paths[0].endswith("ohsac_only_c2_cand_T98.json")     # never the G13 log of the set
    assert "engine" not in only and "ohs4" not in only
    json.dumps(only)


def test_ac_only_seed_run_quarantines_like_the_full_seed_run(acw):
    full = run_ac(acw, "seed")["c2_seed_T98"]
    only = G.run_ohsac_only("seed", ["T98"], write=False, prereg_text=acw["ac"]["prereg"])["c2_seed_T98"]
    assert sorted(x["template_id"] for x in only["quarantine"]) == sorted(x["template_id"] for x in full["quarantine"])
    assert only["quarantine_templates"] == full["quarantine_templates"] == 7


def test_ac_only_run_is_incomplete_without_the_union_record(acw):
    (acw["ac"]["union"] / "RECORD.json").unlink()
    only = G.run_ohsac_only("candidates", ["T98"], write=False, prereg_text=acw["ac"]["prereg"])["c2_cand_T98"]
    assert only["ohsac_complete"] is False and set(only["drop_ids"]) == {"r1", "r2"}


# ------------------------------------------------------------------------------------------------ program text beyond the CODE_FILES
def test_other_program_text_files_are_compared_in_the_ac_step_only(acw):
    blk = acw["pools"].parent
    (blk / "texts.py").write_text('RULE = "ACTPL fixed program wording with enough words in it."\nOK = "A harmless fixed wording with enough words."\n')
    full = run_ac(acw, "candidates")["c2_cand_T98"]
    lits = full["ohsac"]["program_literal_hits"]
    assert any(k.startswith("ac_seed:") and k.endswith("texts.py#0") for k in lits), lits
    assert not any(k.endswith("texts.py#1") for k in lits)
    assert full["ohsac"]["program_literals"] == 5 and full["code_seed_literals"] == 3          # the engine's count is unchanged
    assert any(n == "texts.py" for n in full["inputs_at_start"])                              # the run-input guard holds the file


def test_a_program_only_seed_block_has_a_seed_stage_in_the_ac_only_run(acw):
    blk = acw["pools"].parent.parent / "T97"
    blk.mkdir()
    (blk / "texts.py").write_text('RULE = "Dear {NAME}, ' + SUITE_LONG + '"\nOK = "A harmless fixed wording with enough words."\n'
                                  'KW = "Ship it with ' + SUITE_KEYWORD + ' on Friday."\n')
    (blk / "plugin.py").write_text('CARD = "Use the ledger rules to decide which payment arrives first."\n')
    with pytest.raises(SystemExit):                                                 # a full seed run needs a pool: skipped, as before
        G.run("seed", ["T97"], embed=False, side=False, tgs=acw["tgs"], exports=acw["exports"], write=False,
              prereg_text=acw["ac"]["prereg"], ohsac=True)
    only = G.run_ohsac_only("seed", ["T97"], write=False, prereg_text=acw["ac"]["prereg"])["c2_seed_T97"]
    assert only["units"] == 0 and only["ohsac_complete"] and only["quarantine_templates"] == 2
    assert sorted(x["template_id"].rsplit("#", 1)[0].split("/")[-1] for x in only["quarantine"]) == ["texts.py", "texts.py"]
    assert only["ohsac"]["hit_units"] == 0 and len(only["ohsac"]["program_literal_hits"]) == 2
