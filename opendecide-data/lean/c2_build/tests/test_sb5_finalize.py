"""Tests for the SB5 QC record writer (zed_orch/sb_blocks/SB5/tools/sb5_finalize.py; Ruling A66 a, b).
Fixtures are COPIES of SB5's small files in a pytest tmp dir (the archive and the bench pins are read-only inputs); nothing under
lean/data is written. Every new check has a fault-injection test: the untouched copy passes it, the injected fault fails it.
Run from lean/:  ../.venv/bin/python -B -m pytest -q c2_build/tests/test_sb5_finalize.py
"""
from __future__ import annotations

import copy
import json
import os
import shutil
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
TOOLS = C2B / "zed_orch/sb_blocks/SB5/tools"
sys.path.insert(0, str(C2B)); sys.path.insert(0, str(TOOLS))
import sb5_finalize as fin  # noqa: E402
from sb5_lib import LEAN, SB5, sha  # noqa: E402

REAL_PART = LEAN / "data/c2_parts/SB5"
NOW = "2026-10-17T09:30:00+00:00"


def cp(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def make_tree(root: Path) -> fin.Ctx:
    """A copy of every mutable input of the writer under root/; the archive and the pin data are shared read-only."""
    lean, sb5, c2 = root / "lean", root / "sb5", root / "lean/c2_build"
    for rel in ("out/MANIFEST.json", "out/candidates_c2.jsonl", "out/candidates_c2.relations.jsonl", "hold_owndev/mixdev_S5.jsonl", "qc/QC_REPORT.json"):
        cp(REAL_PART / rel, lean / "data/c2_parts/SB5" / rel)
    shutil.copytree(LEAN / "data/c2_crowd_shards/SB5", lean / "data/c2_crowd_shards/SB5")
    cp(LEAN / "data/c_parts/denylist.json", lean / "data/c_parts/denylist.json"); cp(LEAN / "c_src/common/denylist.py", lean / "c_src/common/denylist.py")
    cp(C2B / "gblock/checks/c1_source_names.json", c2 / "gblock/checks/c1_source_names.json")
    cp(C2B / "meta_src/gproxy/SOURCES.json", c2 / "meta_src/gproxy/SOURCES.json")
    for f in ("G1_RECORD.json", "HANDOFF_85_DENYLIST.json", "denylist_query_sb5.json", "denylist_verdict_sb5.json"):
        cp(SB5 / f, sb5 / f)
    shutil.copytree(SB5 / "work", sb5 / "work")
    for rel in ("screen/REPLAY_DENY_A46.json", "screen/REPLAY_UNSCREENED_A46.json", "screen/reads/SCORE.json", "screen/adjudicate/FIRST_PASS.json", "screen/pool/population.jsonl.gz"):
        cp(SB5 / rel, sb5 / rel)
    os.symlink(SB5 / "src", sb5 / "src")                  # the archive: read-only input, shared
    pins = sb5 / "bench_pins"; pins.mkdir()
    cp(SB5 / "bench_pins/SHA256.json", pins / "SHA256.json")
    for d in (SB5 / "bench_pins").iterdir():
        if d.is_dir():
            os.symlink(d, pins / d.name)
    bi = []
    for p, want in fin.binding_inputs(fin.Ctx()):
        q = c2 / "binding" / Path(p).name; cp(p, q); bi.append((q, want))
    return fin.Ctx(sb5=sb5, lean=lean, c2=c2, binding_inputs=tuple(bi), bench=fin.Ctx().bench, arch=fin.Ctx().arch)


@pytest.fixture(scope="session")
def pristine(tmp_path_factory):
    return make_tree(tmp_path_factory.mktemp("sb5_pristine"))


@pytest.fixture()
def tree(tmp_path):
    return make_tree(tmp_path)


def run(ctx, *names, S=None, mutate=None):
    """Load the state, apply mutate(S, ctx), run the named checks in order (they share S); -> (reasons, S)."""
    R = fin.Rec()
    S = S if S is not None else fin.load_state(ctx, R)
    if mutate:
        mutate(S, ctx)
    for n in names:
        getattr(fin, "check_" + n)(ctx, S, R)
    return R.reasons, S


def has(reasons, needle):
    return any(needle in r for r in reasons)


def wjsonl(path, rows):
    Path(path).write_bytes(("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n").encode("utf-8"))


# ------------------------------------------------------------------ the whole writer on the clean copy

def test_clean_copy_passes_every_check_and_the_mixer_admission(pristine):
    qc, R = fin.evaluate(pristine, NOW)
    assert R.reasons == [] and qc["pass"] is True and qc["passed_utc"] == NOW and qc["fix_iterations"] == 0
    assert qc["files"]["candidates_c2.jsonl"]["rows"] == 1039 and qc["mixdev"]["mixdev_S5.jsonl"]["rows"] == 137
    assert set(qc["rederived_checks"]) == {"files", "gates", "g1", "provenance", "a46", "handoff", "crowd", "selection", "dev", "bench"}
    assert qc["gates_candidates"]["cached_gate_file"]["equals_recomputation"] is True
    assert qc["selection_dry_run"]["a49c_failing_is_binding_for_SB5"] is False
    assert qc["writer"]["sha256"] == sha(fin.WRITER.read_bytes())


def test_gates_pending_lists_g13_ohsac_crowd_selection_a61_final_8_5_and_pilot(pristine):
    qc, _ = fin.evaluate(pristine, NOW, admission=False)
    assert "deferred_gates" not in qc and isinstance(qc["gates_pending"], list)
    txt = " | ".join(qc["gates_pending"])
    for needle in ("G13", "OHS-AC", "crowd selection", "A61 final-mix 8.5", "SB5_uci293", "joint SB pilot", "sob_splits"):
        assert needle in txt, needle


def test_a_fault_gives_pass_false_with_reasons_and_no_passed_utc(tree):
    p = tree.sb5 / "G1_RECORD.json"; g = json.loads(p.read_text()); g["pass"] = False; p.write_text(json.dumps(g))
    qc, R = fin.evaluate(tree, NOW, admission=False)
    assert qc["pass"] is False and qc["passed_utc"] is None and has(qc["reasons_not_passed"], "G1 record pass")


def test_unreadable_input_fails_closed(tree):
    (tree.out / "MANIFEST.json").unlink()
    qc, R = fin.evaluate(tree, NOW, admission=False)
    assert qc["pass"] is False and has(R.reasons, "inputs unreadable")


def test_a_crashing_check_fails_closed(tree):
    (tree.sb5 / "denylist_verdict_sb5.json").write_text("{not json")
    qc, R = fin.evaluate(tree, NOW, checks=(fin.check_files, fin.check_handoff), admission=False)
    assert qc["pass"] is False and has(R.reasons, "check_handoff could not be completed")


def test_now_must_be_utc_iso(tree):
    qc, R = fin.evaluate(tree, "yesterday", checks=(), admission=False)
    assert qc["pass"] is False and has(R.reasons, "--now")


# ------------------------------------------------------------------ line splitting on "\n" only

def test_jsonl_split_on_newline_only():
    rows = [{"id": "a", "state": "x\u2028y\u0085z\x0bw\x0c"}, {"id": "b", "state": "line"}]
    b = ("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n").encode("utf-8")
    assert len(b.decode("utf-8").splitlines()) > 2                       # the old splitlines() miscounted such a file
    assert fin.jl(b) == rows and len(fin.lines(b)) == 2


def test_manifest_row_count_survives_separator_characters(tree):
    cand = [json.loads(l) for l in fin.lines((tree.out / "candidates_c2.jsonl").read_bytes())]
    cand[0]["state"] = cand[0]["state"] + "\u2028\u0085"
    wjsonl(tree.out / "candidates_c2.jsonl", cand)
    shutil.copy(tree.out / "candidates_c2.jsonl", tree.work / "candidates_screened.jsonl")
    man = json.loads((tree.out / "MANIFEST.json").read_text())
    man["files"]["candidates_c2.jsonl"] = {"sha256": sha((tree.out / "candidates_c2.jsonl").read_bytes()), "rows": len(cand)}
    (tree.out / "MANIFEST.json").write_text(json.dumps(man))
    reasons, _ = run(tree, "files")
    assert not has(reasons, "rows, MANIFEST") and not has(reasons, "sha256 differs")


# ------------------------------------------------------------------ check_files

def test_files_clean(pristine):
    assert run(pristine, "files")[0] == []

def test_files_manifest_sha_mismatch_bites(tree):
    man = json.loads((tree.out / "MANIFEST.json").read_text()); man["files"]["candidates_c2.jsonl"]["sha256"] = "0" * 64
    (tree.out / "MANIFEST.json").write_text(json.dumps(man))
    assert has(run(tree, "files")[0], "sha256 differs from the MANIFEST")

def test_files_not_the_screened_work_file_bites(tree):
    (tree.work / "candidates_screened.jsonl").write_bytes(b"")
    assert has(run(tree, "files")[0], "not the A46-screened work file")

def test_files_relations_must_be_empty(tree):
    (tree.out / "candidates_c2.relations.jsonl").write_bytes(b'{"a": 1}\n')
    assert has(run(tree, "files")[0], "relations file has rows")

def test_files_below_target_bites(tree):
    rows = fin.jl((tree.out / "candidates_c2.jsonl").read_bytes())[:700]
    wjsonl(tree.out / "candidates_c2.jsonl", rows); shutil.copy(tree.out / "candidates_c2.jsonl", tree.work / "candidates_screened.jsonl")
    assert has(run(tree, "files")[0], "< the 750-row target")


# ------------------------------------------------------------------ check_gates: recomputed, cache sha-bound

def test_gates_recomputed_pass_and_equal_cache(pristine):
    reasons, S = run(pristine, "gates")
    assert reasons == [] and S["gates"]["candidates"]["tokens"]["counted_by"] == fin.PINNED_TOKENIZER

def test_gates_stale_cached_pass_cannot_mask_a_real_failure(tree):
    """A duplicated row: the cached gates_*_screened.json still says pass (stale), the recomputation must fail."""
    rows = fin.jl((tree.out / "candidates_c2.jsonl").read_bytes()); rows.append(rows[0])
    wjsonl(tree.out / "candidates_c2.jsonl", rows)
    assert json.loads((tree.work / "gates_candidates_screened.json").read_text())["pass"] is True
    reasons, _ = run(tree, "gates")
    assert has(reasons, "format gates not 100% on the candidates (recomputed)") and has(reasons, "differs from the recomputed gates")

def test_gates_cache_tamper_bites_even_when_the_data_is_fine(tree):
    p = tree.work / "gates_owndev_screened.json"; g = json.loads(p.read_text()); g["tokens"]["mean"] = 1.0; p.write_text(json.dumps(g))
    assert has(run(tree, "gates")[0], "cached gates_owndev_screened.json differs")

def test_gates_prescreen_failure_breaks_the_fix_iterations_basis(tree):
    p = tree.work / "gates_candidates.json"; g = json.loads(p.read_text()); g["failures"]["schema"] = 3; p.write_text(json.dumps(g))
    assert has(run(tree, "gates")[0], "fix_iterations basis")

def test_gates_row_count_guard_bites(tree):
    """sb5_gates reads text-mode lines; a file whose \"\\n\"-split count differs from what the gate tool read is a reason."""
    import sb5_gates
    real = sb5_gates.run
    try:
        sb5_gates.run = lambda path: dict(real(path), rows=1)
        assert has(run(tree, "gates")[0], "gate tool read 1 rows")
    finally:
        sb5_gates.run = real

def test_gates_unpinned_tokenizer_bites(tree):
    import sb5_gates
    real = sb5_gates.run
    def fake(path):
        g = real(path); g["tokens"] = dict(g["tokens"], counted_by="approx"); return g
    try:
        sb5_gates.run = fake
        assert has(run(tree, "gates")[0], "pinned tokenizer")
    finally:
        sb5_gates.run = real


# ------------------------------------------------------------------ G1 and row provenance

def test_g1_clean(pristine):
    assert run(pristine, "g1")[0] == []

@pytest.mark.parametrize("edit,needle", [
    (lambda g: g.__setitem__("pass", False), "G1 record pass"),
    (lambda g: g["licence"].__setitem__("spdx", "GPL-2.0"), "G1 licence"),
    (lambda g: g["licence"].__setitem__("commercial_use_allowed", "no"), "G1 licence"),
    (lambda g: g["A58_a_checks"].__setitem__("a3_human_text_and_labels_only", "FAIL"), "a3_human_text_and_labels_only"),
    (lambda g: g["sha256"].__setitem__("uci293.zip", "0" * 64), "zip sha256 on disk differs"),
    (lambda g: g["dataset"].__setitem__("uci_id", 1), "not the SB5 / UCI 293 record"),
])
def test_g1_faults_bite(tree, edit, needle):
    p = tree.sb5 / "G1_RECORD.json"; g = json.loads(p.read_text()); edit(g); p.write_text(json.dumps(g))
    assert has(run(tree, "g1")[0], needle)

def test_provenance_clean(pristine):
    assert run(pristine, "g1", "provenance")[0] == []

@pytest.mark.parametrize("field,edit,needle", [
    ("cand", lambda r: r.__setitem__("gold", 1 - r["gold"]), "gold_not_polarity_x_label"),
    ("cand", lambda r: r.__setitem__("state", r["state"] + " x"), "state_differs_from_archive_text"),
    ("dev", lambda r: r["meta"]["sb5"].__setitem__("orig_label", "negative" if r["meta"]["sb5"]["orig_label"] == "positive" else "positive"), "label_differs_from_archive_dir"),
    ("cand", lambda r: r["meta"]["sb5"].__setitem__("uci_rid", "positive99999"), "rid_not_in_archive"),
    ("cand", lambda r: r["meta"]["sb5"]["provenance"].__setitem__("zip_sha256", "0" * 64), "row_zip_rar_sha_differs_from_G1"),
    ("cand", lambda r: r["meta"].__setitem__("licence", "MIT"), "licence_not_cc_by_4"),
])
def test_provenance_faults_bite(pristine, field, edit, needle):
    def mut(S, ctx):
        S[field] = copy.deepcopy(S[field]); edit(S[field][5])
    reasons, _ = run(pristine, "g1", "provenance", mutate=mut)
    assert has(reasons, needle)


# ------------------------------------------------------------------ A46

def test_a46_clean(pristine):
    reasons, S = run(pristine, "a46")
    assert reasons == [] and S["apply"]["candidates"] == [1124, 1039, 85] and S["apply"]["owndev"] == [150, 137, 13]

def test_a46_dropped_id_still_present_bites(pristine):
    def mut(S, ctx):
        S["cand"] = S["cand"] + [S["raw_cand"][[r["id"] for r in S["raw_cand"]].index(sorted(json.loads((ctx.screen / "REPLAY_DENY_A46.json").read_text())["drop_ids"])[0])]]
    assert has(run(pristine, "a46", mutate=mut)[0], "still in the final candidates or own dev")

def test_a46_relabel_of_a_kept_row_bites(pristine):
    def mut(S, ctx):
        rows = copy.deepcopy(S["cand"]); rows[3]["gold"] = 1 - rows[3]["gold"]
        S["cand_b"] = ("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n").encode("utf-8"); S["cand"] = rows
    assert has(run(pristine, "a46", mutate=mut)[0], "not byte-equal to the raw rows")

def test_a46_raw_minus_screened_must_be_exactly_the_drops(pristine):
    def mut(S, ctx):
        S["cand"] = S["cand"][:-1]
    assert has(run(pristine, "a46", mutate=mut)[0], "raw minus screened is not exactly the A46 drop ids")

def test_a46_inputs_sha_mismatch_bites(tree):
    p = tree.sb5 / "screen/reads/SCORE.json"; p.write_bytes(p.read_bytes() + b" ")
    assert has(run(tree, "a46")[0], "inputs_sha256 differs")

def test_a46_unscreened_rows_bite(tree):
    p = tree.sb5 / "screen/REPLAY_UNSCREENED_A46.json"; d = json.loads(p.read_text()); d["drop_ids"] = ["c2_sb5:positive1:pos"]; p.write_text(json.dumps(d))
    assert has(run(tree, "a46")[0], "unscreened rows remain")

def test_a46_incomplete_reads_bite(tree):
    p = tree.sb5 / "screen/reads/SCORE.json"; d = json.loads(p.read_text()); d["n_incomplete"] = 2; p.write_text(json.dumps(d))
    reasons, _ = run(tree, "a46")
    assert has(reasons, "read score does not cover every raw row") or has(reasons, "inputs_sha256 differs")

def test_a46_cached_apply_report_must_match_recomputation(tree):
    p = tree.work / "apply_report.json"; d = json.loads(p.read_text()); d["owndev"] = [150, 140, 10]; p.write_text(json.dumps(d))
    assert has(run(tree, "a46")[0], "apply_report.json differs from the recomputed")


# ------------------------------------------------------------------ handoff, deny-list, 8.5 inputs, C1 / G-proxy names

def test_handoff_clean(pristine):
    assert run(pristine, "handoff")[0] == []

def _edit(path, fn):
    d = json.loads(path.read_text()); fn(d); path.write_text(json.dumps(d))

@pytest.mark.parametrize("file,fn,needle", [
    ("HANDOFF_85_DENYLIST.json", lambda d: d["orchestrator_verdict"].__setitem__("8.5", "HIT"), "8.5 sealed-side"),
    ("HANDOFF_85_DENYLIST.json", lambda d: d["orchestrator_verdict"].__setitem__("denylist", "FAIL"), "deny-list handoff verdict"),
    ("HANDOFF_85_DENYLIST.json", lambda d: d["orchestrator_verdict"].__setitem__("gproxy_source", "HIT"), "G-proxy handoff verdict"),
    ("HANDOFF_85_DENYLIST.json", lambda d: d["orchestrator_actions"][0].__setitem__("result", "HIT"), "handoff action 8.5"),
    ("denylist_verdict_sb5.json", lambda d: d["counts"].__setitem__("deny_taint", 1), "not a clean pass"),
    ("denylist_verdict_sb5.json", lambda d: d["verdicts"]["sb5_uci293_ar_twitter"].__setitem__("verdict", "deny"), "not pass"),
    ("denylist_verdict_sb5.json", lambda d: d.__setitem__("query_sha256", "0" * 64), "query_sha256 differs"),
    ("denylist_verdict_sb5.json", lambda d: d.__setitem__("denylist_sha256", "0" * 64), "another deny-list"),
    ("denylist_verdict_sb5.json", lambda d: d.__setitem__("canonical", False), "not a canonical sb5 run"),
])
def test_handoff_faults_bite(tree, file, fn, needle):
    _edit(tree.sb5 / file, fn)
    assert has(run(tree, "handoff")[0], needle)

def test_handoff_query_changed_after_the_verdict_bites(tree):
    _edit(tree.sb5 / "denylist_query_sb5.json", lambda d: d["datasets"]["sb5_uci293_ar_twitter"]["names"].append("another name"))
    assert has(run(tree, "handoff")[0], "query_sha256 differs")

def test_handoff_85_binding_input_pin_bites(tree):
    p = Path(tree.binding_inputs[1][0]); p.write_bytes(p.read_bytes() + b" ")
    assert has(run(tree, "handoff")[0], "8.5 binding input")

def test_handoff_85_binding_input_without_the_source_bites(tree):
    p = Path(tree.binding_inputs[1][0]); _edit(p, lambda d: d["sources"][0].__setitem__("id", "OTHER"))
    tree.binding_inputs = ((tree.binding_inputs[0]), (p, sha(p.read_bytes())))
    assert has(run(tree, "handoff")[0], "does not carry the SB5 source")

def test_c1_source_name_hit_bites(tree):
    _edit(tree.c1_names, lambda d: d["names"].append("Arabic sentiment corpus (UCI 293)"))
    assert has(run(tree, "handoff")[0], "C1 source names")

def test_c1_generic_word_alone_is_not_a_hit(pristine):
    assert "tweet" in fin.GENERIC_TERMS and run(pristine, "handoff")[0] == []

def test_gproxy_host_collision_bites(tree):
    _edit(tree.gproxy, lambda d: d["sources"].append({"id": "gp_x", "name": "Other", "host": "archive.ics.uci.edu"}))
    assert has(run(tree, "handoff")[0], "G-proxy source check")


# ------------------------------------------------------------------ crowd labels

def test_crowd_clean(pristine):
    reasons, S = run(pristine, "a46", "crowd")
    assert reasons == [] and S["crowd"]["p_g_lt_0.05_pre_a46"] == 1 and S["crowd"]["p_g_lt_0.05_dropped_by_a46"] == 1
    assert S["crowd"]["bin_shares_final"]["easy"] == 0.0

def test_crowd_missing_label_bites(pristine):
    def mut(S, ctx):
        S["cand"] = S["cand"] + [dict(S["cand"][0], id="c2_sb5:positive_new:pos")]
    reasons, _ = run(pristine, "a46", "crowd", mutate=mut)
    assert has(reasons, "crowd labels cover")

def test_crowd_stale_candidates_sha_bites(tree):
    p = tree.crowd_dir / "shards.json"; d = json.loads(p.read_text()); d["candidates_sha256"] = "0" * 64; p.write_text(json.dumps(d))
    assert has(run(tree, "a46", "crowd")[0], "candidates_sha256 is not the raw")

def _relabel(tree, fn):
    """Rewrite the crowd probabilities of the final candidates: fn(gold) -> (p_yes, p_no)."""
    lp = tree.labels_dir / "shard_000.jsonl"
    rows = [json.loads(l) for l in lp.read_text().split("\n") if l.strip()]
    cand = {x["id"]: x for x in fin.jl((tree.out / "candidates_c2.jsonl").read_bytes())}
    n = 0
    for r in rows:
        g = cand.get(r["id"])
        if g is not None:
            y = fn(g["gold"], n); r["probs"] = {"yes": y, "no": round(1 - y, 6)}; n += 1
    wjsonl(lp, rows)

def test_crowd_hard_bar_bites(tree):
    """Labels that put 40% of the final candidates in the hard bin (p_g <= 0.30) break the 30% bar."""
    _relabel(tree, lambda gold, n: (0.2 if gold == 1 else 0.8) if n % 5 < 2 else (0.6 if gold == 1 else 0.4))   # n % 5 < 2: wrong side, p_g = 0.2
    assert has(run(tree, "a46", "crowd")[0], "step-10 crowd bars")

def test_crowd_easy_bar_bites(tree):
    _relabel(tree, lambda gold, n: 0.99 if gold == 1 else 0.01)
    assert has(run(tree, "a46", "crowd")[0], "step-10 crowd bars")

def test_crowd_low_pg_row_that_stayed_bites(tree):
    _relabel(tree, lambda gold, n: (0.99 if gold == 0 else 0.01) if n == 0 else (0.6 if gold == 1 else 0.4))
    assert has(run(tree, "a46", "crowd")[0], "final candidates have p_g < 0.05")

def test_crowd_low_pg_row_not_dropped_by_a46_bites(tree):
    p = tree.sb5 / "screen/REPLAY_DENY_A46.json"; d = json.loads(p.read_text())
    d["drop_ids"] = [i for i in d["drop_ids"] if i != "c2_sb5:negative390:neg"]; p.write_text(json.dumps(d))
    assert has(run(tree, "a46", "crowd")[0], "were not dropped by A46")

def test_crowd_cached_summary_must_match(tree):
    _edit(tree.work / "crowd_summary.json", lambda d: d.__setitem__("p_g_lt_0.05", 0))
    assert has(run(tree, "a46", "crowd")[0], "crowd_summary.json differs")


# ------------------------------------------------------------------ selection dry run

def test_selection_clean(pristine):
    reasons, S = run(pristine, "a46", "crowd", "selection")
    assert reasons == [] and S["sel"]["selected"] == 750 and 0.45 <= S["sel"]["yes_share"] <= 0.55
    assert S["sel"]["a49c_failing_is_binding_for_SB5"] is False and S["sel"]["a49c_failing"]

def test_selection_cached_file_must_match(tree):
    _edit(tree.work / "select_dry.json", lambda d: d.__setitem__("yes_share", 0.5))
    assert has(run(tree, "a46", "crowd", "selection")[0], "select_dry.json differs")

def test_selection_yes_share_band_bites(pristine):
    S = run(pristine, "a46", "crowd")[1]
    S = dict(S); rows = copy.deepcopy(S["cand"])
    for k, r in enumerate(rows):
        if r["gold"] == 1 and k % 3:
            r["gold"] = 0
    S["cand"] = rows
    R = fin.Rec(); fin.check_selection(pristine, S, R)
    assert has(R.reasons, "yes share") or has(R.reasons, "selects")

def test_selection_a49c_binds_when_sb5_is_in_the_binding_set(pristine, monkeypatch):
    monkeypatch.setattr(fin, "a49c_blocks", lambda: ("SB5",))
    reasons, _ = run(pristine, "a46", "crowd", "selection")
    assert has(reasons, "A49 c checks fail on the selected rows and bind for SB5")


# ------------------------------------------------------------------ own dev

def test_dev_clean(pristine):
    assert run(pristine, "dev")[0] == []

def test_dev_over_150_bites(pristine):
    def mut(S, ctx):
        S["dev"] = [copy.deepcopy(S["dev"][i % len(S["dev"])]) for i in range(151)]
    assert has(run(pristine, "dev", mutate=mut)[0], "> 150")

def test_dev_shared_source_record_bites(pristine):
    def mut(S, ctx):
        S["dev"] = copy.deepcopy(S["dev"]); S["dev"][0]["meta"]["sb5"]["uci_rid"] = S["cand"][0]["meta"]["sb5"]["uci_rid"]
    assert has(run(pristine, "dev", mutate=mut)[0], "share a source record")

def test_dev_shared_normalised_text_bites(pristine):
    """Different ids and records, the same tweet up to tashkeel / URL / mention / alef variants."""
    def mut(S, ctx):
        S["dev"] = copy.deepcopy(S["dev"]); S["dev"][0]["state"] = "@user " + S["cand"][0]["state"] + " http://t.co/x"
    assert has(run(pristine, "dev", mutate=mut)[0], "share a normalised text")

def test_dev_holdout_redraw_bites(tree):
    p = tree.work / "pool.json"; d = json.loads(p.read_text()); d["dev_ids"][0], d["dev_ids"][1] = d["dev_ids"][1], d["dev_ids"][0]; p.write_text(json.dumps(d, ensure_ascii=False))
    assert has(run(tree, "dev")[0], "seeded (20261013)")


# ------------------------------------------------------------------ bench exclusion

def test_bench_clean(pristine):
    reasons, S = run(pristine, "bench")
    assert reasons == [] and S["bench"]["final_rows_hit"] == {} and S["bench"]["self_test"]["exact_hits"] == 40

def test_bench_pin_text_in_a_candidate_bites(pristine):
    import gzip
    seg = next(json.loads(l)["text"] for l in gzip.open(pristine.pins / "mteb__tweet_sentiment_multilingual/test/arabic.jsonl.gz", "rt", encoding="utf-8")
               if len(fin.norm_tokens(json.loads(l)["text"])) >= 8)
    def mut(S, ctx):
        S["cand"] = copy.deepcopy(S["cand"]); S["cand"][0]["state"] = seg
    assert has(run(pristine, "bench", mutate=mut)[0], "final rows hit a bench / pin / C2-dev index")

def test_bench_near_copy_in_own_dev_bites(pristine):
    import gzip
    seg = next(json.loads(l)["text"] for l in gzip.open(pristine.pins / "mteb__tweet_sentiment_multilingual/test/arabic.jsonl.gz", "rt", encoding="utf-8")
               if len(fin.norm_tokens(json.loads(l)["text"])) >= 8)
    def mut(S, ctx):
        S["dev"] = copy.deepcopy(S["dev"]); S["dev"][0]["state"] = " ".join(seg.split()[1:])
    assert has(run(pristine, "bench", mutate=mut)[0], "owndev:")

def test_bench_pin_sha_mismatch_bites(tree):
    _edit(tree.pins / "SHA256.json", lambda d: d.__setitem__("mteb/tweet_sentiment_multilingual:test/arabic.jsonl.gz", "0" * 64))
    assert has(run(tree, "bench")[0], "bench pin mteb/tweet_sentiment_multilingual")

def test_bench_prep_drops_must_be_empty(tree):
    _edit(tree.work / "prep_report.json", lambda d: d.__setitem__("bench_dev_exclusion_drops", {"bench_cases:exact": 2}))
    assert has(run(tree, "bench")[0], "prep step dropped source rows")

def test_bench_target_changed_since_prep_bites(tree):
    _edit(tree.work / "prep_report.json", lambda d: d["target_arabic_segments"].__setitem__("bench_cases", 1))
    assert has(run(tree, "bench")[0], "bench or pin changed")


# ------------------------------------------------------------------ admission self-check

def test_admission_check_catches_a_stale_sha(pristine):
    qc, _ = fin.evaluate(pristine, NOW, admission=False)
    assert fin.admission_check(pristine, qc) == []
    bad = copy.deepcopy(qc); bad["files"]["candidates_c2.jsonl"]["sha256"] = "0" * 64
    assert fin.admission_check(pristine, bad)
    late = dict(qc, passed_utc="2026-10-22T00:00:00+00:00")
    assert fin.admission_check(pristine, late)


# ------------------------------------------------------------------ write safety: backup first, atomic, nothing else touched

def _guard(ctx):
    return {p: sha(Path(p).read_bytes()) for p in (ctx.out / "candidates_c2.jsonl", ctx.out / "candidates_c2.relations.jsonl", ctx.dev_path, ctx.out / "MANIFEST.json")}

def test_write_backs_up_first_then_replaces_atomically(tree):
    old = tree.qc_path.read_bytes()
    qc, _ = fin.evaluate(tree, NOW, admission=False)
    s = fin.write_record(tree, qc, _guard(tree))
    bak = next(tree.backup_dir.glob("QC_REPORT.before_write_*.json"))
    assert bak.read_bytes() == old and sha(old)[:12] in bak.name
    assert sha(tree.qc_path.read_bytes()) == s and json.loads(tree.qc_path.read_text())["pass"] is True
    assert not list(tree.qc_path.parent.glob("*.tmp"))

def test_write_refused_when_the_backup_cannot_be_made(tree):
    old = tree.qc_path.read_bytes()
    tree.backup_dir.parent.mkdir(parents=True, exist_ok=True); tree.backup_dir.write_text("a file, not a directory")
    qc, _ = fin.evaluate(tree, NOW, admission=False)
    with pytest.raises(fin.WriteRefused):
        fin.write_record(tree, qc, _guard(tree))
    assert tree.qc_path.read_bytes() == old

def test_write_refused_when_a_different_backup_of_the_same_name_exists(tree):
    old = tree.qc_path.read_bytes()
    tree.backup_dir.mkdir(parents=True)
    (tree.backup_dir / f"QC_REPORT.before_write_{sha(old)[:12]}.json").write_bytes(b"other content")
    qc, _ = fin.evaluate(tree, NOW, admission=False)
    with pytest.raises(fin.WriteRefused):
        fin.write_record(tree, qc, _guard(tree))
    assert tree.qc_path.read_bytes() == old

def test_write_refuses_any_other_target(tree):
    qc, _ = fin.evaluate(tree, NOW, admission=False)
    tree.qc_path = tree.part / "qc" / "OTHER.json"
    with pytest.raises(fin.WriteRefused):
        fin.write_record(tree, qc, _guard(tree))

def test_write_does_not_touch_out_or_dev(tree):
    g = _guard(tree); qc, _ = fin.evaluate(tree, NOW, admission=False)
    fin.write_record(tree, qc, g)
    assert _guard(tree) == g

def test_write_detects_a_changed_guard_file(tree):
    g = _guard(tree); qc, _ = fin.evaluate(tree, NOW, admission=False)
    g[tree.dev_path] = "0" * 64
    with pytest.raises(fin.WriteRefused):
        fin.write_record(tree, qc, g)

def test_default_run_is_dry_and_write_needs_the_flag(monkeypatch, capsys):
    called = []
    monkeypatch.setattr(fin, "write_record", lambda *a, **k: called.append(1) or "x")
    qc = {"pass": True, "passed_utc": NOW, "fix_iterations": 0, "reasons_not_passed": [], "files": {}, "gates_pending": [1], "writer": {"sha256": "w"}}
    monkeypatch.setattr(fin, "evaluate", lambda ctx, now: (qc, fin.Rec()))
    fin.main(["--now", NOW])
    assert called == [] and json.loads(capsys.readouterr().out)["dry"] is True
    fin.main(["--now", NOW, "--write"])
    assert called == [1]
    with pytest.raises(SystemExit):
        fin.main(["--write", "--dry"])

def test_dry_out_never_the_real_record(monkeypatch):
    monkeypatch.setattr(fin, "evaluate", lambda ctx, now: ({"pass": True, "passed_utc": NOW, "fix_iterations": 0, "reasons_not_passed": [], "files": {}, "gates_pending": [], "writer": {"sha256": "w"}}, fin.Rec()))
    with pytest.raises(SystemExit):
        fin.main(["--dry-out", str(REAL_PART / "qc/QC_REPORT.json")])
