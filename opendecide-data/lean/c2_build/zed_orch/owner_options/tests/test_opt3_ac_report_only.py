"""Tests for owner option 3 (ac_report_only.py + ruling_gate.py + the three *_opt3.py wrappers). Synthetic data only: synthetic PREREG text,
synthetic G13 logs under tmp_path, test_g13_c2.py's `world` (fake OHS-4 tools, synthetic exports) with a FAKE OHS-AC side and fake OHS-AC
checkers defined here. No sealed, "ohs" or Jev path is opened; the real PREREG_FINAL.md is read (a C2-side doc) by one test. Run from lean/:
  ../.venv/bin/python -B -m pytest -q c2_build/zed_orch/owner_options/tests/test_opt3_ac_report_only.py
"""
from __future__ import annotations

import json
import sys
import types
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
OPT = Path(__file__).resolve().parents[1]
C2B = OPT.parents[1]
for p in (str(OPT), str(C2B), str(C2B / "tests")):
    sys.path.insert(0, p)
import ac_report_only as opt3  # noqa: E402
import c2_select as sel  # noqa: E402
import c2io  # noqa: E402
import g13_c2 as G  # noqa: E402
import mix_c2 as m  # noqa: E402
import ruling_gate as rg  # noqa: E402
from test_c2_select import g13_log, g13w  # noqa: E402,F401  (fixtures: isolated layout, guarded synthetic G13 logs)
from test_g13_c2 import A38, SUITE_KEYWORD, exports, fake_tools, row, world  # noqa: E402,F401

OWNER_RULING = ("> **Ruling A68 (17 Oct 2026, ~12:00 UTC; owner decision in chat; orchestrator, Opus).** OHS-AC is "
                "report-only for C2;\n> OHS-4 stays binding.\n> Machine marker for the A68 switch (owner_options/, Option 3): OHSAC_REPORT_ONLY.\n")
PREREG = ("> **Ruling A64 (17 Oct 2026; orchestrator, Opus; revision 3).** (a) no excusal. OHS-AC report-only is NOT adopted here.\n"
          "> (b) more text.\n"
          "> **Ruling A65 (17 Oct 2026; orchestrator).** other.\n\n"
          + OWNER_RULING + "\n"
          "> **Ruling A69 (owner, 17 Oct 2026).** frame text.\n> Machine marker: OHSAC_FRAME_EXCUSE.\n\n"
          "> **Ruling A70 (orchestrator; orchestrator alone).** x\n> Machine marker: OHSAC_REPORT_ONLY\n\n"
          "> **Ruling A71 (owner).** x\n> Machine marker: OHSAC_REPORT_ONLY\n\n> **Ruling A71 (owner).** again\n> Machine marker: OHSAC_REPORT_ONLY\n\n"
          "> **Ruling A72 (owner decision).** something else entirely.\n\n"
          "> **Ruling A73 (owner).** OHSAC_REPORT_ONLY is NOT adopted here (prose mention, no machine marker line).\n\n"
          "> **Ruling A74 (owner).** x\n> Machine marker: XOHSAC_REPORT_ONLY_V2 and OHSAC_REPORT_ONLYX.\n\n"
          "> **Ruling A75 (owner).** x\n> A machine marker would go here: OHSAC_REPORT_ONLY.\n")


# ------------------------------------------------------------------------------------------------ the ruling gate
def test_gate_accepts_only_an_owner_ruling_that_carries_the_marker():
    info = rg.require("A68", rg.OPT3_MARKER, PREREG)
    assert info["id"] == "A68" and len(info["block_sha256"]) == 64 and len(info["prereg_sha256"]) == 64
    for rid, why in (("A99", "no ruling block"), ("A64", "owner"), ("A65", "owner"), ("A72", "marker"), ("A69", "marker"), ("A70", "owner"),
                     ("A71", "ambiguous"), ("A73", "marker"), ("A74", "marker"), ("A75", "marker"), ("68", "not a ruling id"), ("", "not a ruling id"), (None, "not a ruling id"),
                     ("A68; rm", "not a ruling id")):
        with pytest.raises(rg.RulingRefused) as e:
            rg.require(rid, rg.OPT3_MARKER, PREREG)
        assert why in str(e.value) and "stays OFF" in str(e.value), (rid, str(e.value))
    assert rg.require("A69", rg.FRAME_MARKER, PREREG)["marker"] == rg.FRAME_MARKER
    with pytest.raises(rg.RulingRefused):
        rg.require("A68", rg.KW_MARKER, PREREG)               # a ruling for one option never arms another
    with pytest.raises(rg.RulingRefused):
        rg.require("A68", "SOMETHING", PREREG)


def test_gate_accepts_a68_and_nothing_else_in_the_real_prereg():
    """PREREG_FINAL.md carries the A68 machine marker (17 Oct, owner ruling): A68 arms option 3 only; no other id arms any option; A68 arms no
    other option (a ruling for one option never arms another)."""
    text = Path(c2io.PREREG).read_text(encoding="utf-8")
    blocks = rg.ruling_blocks(text)
    assert len(blocks) >= 30 and "A64" in blocks and "A38" in blocks and len(blocks["A68"]) == 1       # the parser sees the real blocks
    info, why = rg.check("A68", rg.OPT3_MARKER, text)
    assert why is None and info["id"] == "A68" and len(info["block_sha256"]) == 64
    assert rg.check("A68", rg.FRAME_MARKER, text)[0] is None and rg.check("A68", rg.KW_MARKER, text)[0] is None
    for mk in rg.MARKERS:
        for rid in blocks:
            if (rid, mk) != ("A68", rg.OPT3_MARKER):
                assert rg.check(rid, mk, text)[0] is None, (rid, mk)


def test_marker_is_a_whole_token_on_a_machine_marker_line_only():
    assert rg.has_marker("> x\n> Machine marker: OHSAC_REPORT_ONLY.", rg.OPT3_MARKER)
    assert rg.has_marker("> Machine marker for the A68 switch (a/b, Option 3): OHSAC_REPORT_ONLY", rg.OPT3_MARKER)
    for bad in ("> OHSAC_REPORT_ONLY alone on a prose line", "> Machine marker: XOHSAC_REPORT_ONLY", "> Machine marker: OHSAC_REPORT_ONLY_2",
                "> Machine marker: OHSAC_REPORT_ONLYX", "> no marker", "> Machine marker: OHSAC_FRAME_EXCUSE"):
        assert not rg.has_marker(bad, rg.OPT3_MARKER), bad


def test_pop_flag_refuses_a_repeated_flag():
    for argv in (["--ohsac-report-only", "A68", "--ohsac-report-only", "A70"], ["--ohsac-report-only=A68", "--ohsac-report-only", "A68"],
                 ["--ohsac-report-only", "A68", "--ohsac-report-only=A68"]):
        with pytest.raises(SystemExit) as e:
            rg.pop_flag(argv, "--ohsac-report-only")
        assert "twice" in str(e.value)


def test_pop_flag_forms():
    assert rg.pop_flag(["a", "--ohsac-report-only", "A68", "b"], "--ohsac-report-only") == (["a", "b"], "A68")
    assert rg.pop_flag(["--ohsac-report-only=A68"], "--ohsac-report-only") == ([], "A68")
    assert rg.pop_flag(["a", "b"], "--ohsac-report-only") == (["a", "b"], None)
    with pytest.raises(SystemExit):
        rg.pop_flag(["--ohsac-report-only"], "--ohsac-report-only")
    with pytest.raises(SystemExit):
        rg.pop_flag(["--ohsac-report-only", "--final"], "--ohsac-report-only")


def test_targets_match_g13_c2():
    assert opt3.AC_TARGETS == G.AC_TARGETS


# ------------------------------------------------------------------------------------------------ the split
def units_of(**rows):
    return {k: {"rows": v} for k, v in rows.items()}


def test_classes_are_the_union_of_non_ac_targets_and_an_id_hit_by_both_stays_binding():
    units = units_of(a=["a1", "a2"], b=["b1"], c=["c1"], d=["d1"])
    hits = {"ohs4_hash": {"keyword": {"a": {"state"}}}, "ohsac_hash": {"keyword": {"a": {"state"}, "b": {"state"}}},
            "ohsac_rows": {"exact_seg": {"c": {"sealed"}}}, "c2_mixdev": {"instance": {"d": {"state"}}}}
    cl = opt3.classes_from_hits("candidates", units, hits)
    assert cl["binding"] == ["a1", "a2", "d1"] and cl["ohsac_report_only"] == ["b1", "c1"]
    assert cl["units"] == {"binding": 2, "ohsac_report_only": 2}
    assert cl["capture"]["ac_targets"] == list(G.AC_TARGETS)
    allv = {r for k in ("a", "b", "c", "d") for r in units[k]["rows"]}
    assert set(cl["binding"]) | set(cl["ohsac_report_only"]) == allv
    seed = opt3.classes_from_hits("seed", units, hits)
    assert seed["binding"] == seed["ohsac_report_only"] == []


RULING = {"id": "A68", "marker": rg.OPT3_MARKER, "block_sha256": "b" * 64, "prereg_sha256": "p" * 64}


def sealed(binding, report_only, set_name="c2_cand_X", run="candidates", tool_sha="t" * 64, ruling=RULING, targets=None):
    """A drop_ids_by_class dict as the capture writes it (sealed)."""
    cl = {"binding": list(binding), "ohsac_report_only": list(report_only), "units": {},
          "capture": {"ac_targets": list(targets or G.AC_TARGETS), "module_sha256": "m" * 64}}
    return opt3.seal_classes(cl, {"set": set_name, "run": run, "tool_sha256": tool_sha}, ruling)


def good_log(**kw):
    d = {"set": "c2_cand_X", "run": "candidates", "tool_sha256": "t" * 64, "drop_ids": ["a1", "b1", "c1"], "ohsac": {"complete": True},
         opt3.CLASSES_KEY: sealed(["a1"], ["b1", "c1"])}
    return {**d, **kw}


def test_split_log_modes():
    s = opt3.split_log(good_log())
    assert s["mode"] == "by_class" and s["binding"] == {"a1"} and s["report_only"] == {"b1", "c1"} and s["ruling"]["id"] == "A68"
    old = opt3.split_log({"set": "c2_cand_X", "drop_ids": ["a1", "b1"]})                  # no OHS-AC step in that log
    assert old["mode"] == "no_ac_record" and old["binding"] == {"a1", "b1"} and not old["report_only"]
    plain = opt3.split_log({"drop_ids": ["x"]})
    assert plain["binding"] == {"x"}
    quick = opt3.split_log({"mode": "ohsac_only", "drop_ids": ["a1", "b1"], "ohsac": {}})
    assert quick["mode"] == "ac_only_run" and not quick["binding"] and quick["report_only"] == {"a1", "b1"}


@pytest.mark.parametrize("bad", [
    {opt3.CLASSES_KEY: None},                                                    # OHS-AC record, no split
    {"drop_ids": ["a1", "b1", "c1", "zz"]},                                      # the log changed after the capture
    {"drop_ids": ["a1", "b1"]},                                                  # fewer drops than the split lists
    {opt3.CLASSES_KEY: sealed(["a1", "b1"], ["b1", "c1"])},                       # overlapping classes
    {opt3.CLASSES_KEY: sealed(["a1"], ["b1", "c1"], targets=["ohsac_hash"])},     # other OHS-AC targets
    {opt3.CLASSES_KEY: sealed(["a1"], ["b1", "c1"], set_name="c2_cand_Y")},       # split copied from another set's log
    {opt3.CLASSES_KEY: sealed(["a1"], ["b1", "c1"], run="carry")},                # ... or another run
    {opt3.CLASSES_KEY: sealed(["a1"], ["b1", "c1"], tool_sha="u" * 64)},          # captured by another g13_c2.py
    {opt3.CLASSES_KEY: sealed(["a1"], ["b1", "c1"], ruling=None)},                # captured with no ruling
    {opt3.CLASSES_KEY: {**sealed(["a1"], ["b1", "c1"]), "binding": ["a1", "b1"], "ohsac_report_only": ["c1"]}},   # ids moved after the capture
    {opt3.CLASSES_KEY: {"binding": ["a1"], "ohsac_report_only": ["b1", "c1"], "capture": {"ac_targets": list(G.AC_TARGETS)}}},  # not sealed
    {"drop_ids": None}])
def test_split_log_refuses_what_it_cannot_trust(bad):
    d = {k: v for k, v in good_log(**bad).items() if v is not None}
    with pytest.raises(opt3.SplitRefused):
        opt3.split_log(d)


# ------------------------------------------------------------------------------------------------ select and mix drop sets
def ac_logs(w):
    """Two guarded G13 logs: X has binding {r1}, report-only {r2, r3}; Y has binding {r3, r5}, report-only {r6}."""
    x = g13_log(w, "c2_cand_X1.json", drop_ids=["r1", "r2", "r3"], ohsac={"complete": True},
                drop_ids_by_class=sealed(["r1"], ["r2", "r3"], "c2_cand_X1", "candidates", None))
    y = g13_log(w, "c2_cand_Y1.json", drop_ids=["r3", "r5", "r6"], ohsac={"complete": True},
                drop_ids_by_class=sealed(["r3", "r5"], ["r6"], "c2_cand_Y1", "candidates", None))
    return x, y


def isolate(monkeypatch, mod, names):
    for n in names:
        monkeypatch.setattr(mod, n, getattr(mod, n))
    monkeypatch.setattr(mod, "_opt3", False, raising=False)


def test_select_drop_set_is_the_union_of_non_ac_targets_with_the_flag_and_unchanged_without(g13w, monkeypatch):
    x, y = ac_logs(g13w)
    ilog = c2io.C2InputLog()
    assert sel.drop_ids_of(ilog, [str(x), str(y)]) == {"r1", "r2", "r3", "r5", "r6"}          # without the option: unchanged
    isolate(monkeypatch, sel, ["drop_ids_of"])
    use = opt3.UseLog()
    opt3.install_select(sel, use)
    assert sel.drop_ids_of(c2io.C2InputLog(), [str(x), str(y)]) == {"r1", "r3", "r5"}          # r3 is binding in Y: it stays
    assert sel.drop_ids_of(c2io.C2InputLog(), [str(x)]) == {"r1"}
    assert [r["ohsac_report_only"] for r in use.logs][:2] == [2, 1]
    for r in use.logs:
        assert set(r) >= {"binding_sha256", "ohsac_report_only_sha256", "drop_ids", "binding"} and "r1" not in json.dumps(r)


def test_select_keeps_every_log_check_under_the_option(g13w, monkeypatch):
    x, _y = ac_logs(g13w)
    bad = g13_log(g13w, "c2_cand_Z1.json", drop_ids=["r1"], complete=False, incomplete_why=["method 5 off"])
    isolate(monkeypatch, sel, ["drop_ids_of"])
    opt3.install_select(sel, opt3.UseLog())
    with pytest.raises(SystemExit) as e:
        sel.drop_ids_of(c2io.C2InputLog(), [str(x), str(bad)])
    assert "refused" in str(e.value)
    nosplit = g13_log(g13w, "c2_cand_W1.json", drop_ids=["r1"], ohsac={"complete": True})        # OHS-AC record without the split
    with pytest.raises(opt3.SplitRefused):
        sel.drop_ids_of(c2io.C2InputLog(), [str(nosplit)])


def test_mixer_drop_set_and_the_manifest_block(g13w, monkeypatch, tmp_path):
    x, y = ac_logs(g13w)
    a = types.SimpleNamespace(final=False)
    full, _ = m.g13_drop_ids(a, c2io.C2InputLog(), [str(x), str(y)], [])
    assert full == {"r1", "r2", "r3", "r5", "r6"}
    written, orig_calls = {}, []

    def fake_orig(a_, rep_, rows_, rels_):                                  # the original writer, faked: only its c2io.write_json calls matter
        orig_calls.append(rep_)
        m.c2io.write_json(m.OUT_MAN, {"what": "manifest"})
        m.c2io.write_json(m.WORK / "other.json", {"x": 1})
        return rep_

    isolate(monkeypatch, m, ["g13_drop_ids", "write_outputs", "dry_report", "gated_membership", "binding_ids", "remove_sources"])
    monkeypatch.setattr(m, "write_outputs", fake_orig)
    monkeypatch.setattr(m.c2io, "write_json", lambda p, o, *x_, **k: written.__setitem__(Path(p).name, o) or "sha")
    before = {n: getattr(m, n) for n in ("gated_membership", "binding_ids", "remove_sources", "gate_id")}
    info = rg.require("A68", rg.OPT3_MARKER, PREREG)
    use = opt3.UseLog()
    seeds = tmp_path / "seedlogs"
    seeds.mkdir()
    (seeds / "c2_seed_T27.json").write_text(json.dumps({"quarantine": [
        {"template_id": "t1", "hits": {"ohsac_hash": ["keyword"]}},
        {"template_id": "t2", "hits": {"ohsac_hash": ["keyword"], "ohs4_hash": ["exact_full"]}},
        {"template_id": "t3", "hits": {}}]}))
    opt3.install_mixer(m, info, use, log_dir=seeds)
    probs = []
    ids, used = m.g13_drop_ids(a, c2io.C2InputLog(), [str(x), str(y)], probs)
    assert ids == {"r1", "r3", "r5"} and probs == []
    assert [u["ohsac_report_only_ids"] for u in used] == [2, 1] and [u["binding_ids"] for u in used] == [1, 2]
    for n, f in before.items():                                              # the 8.5 source gate (--exports all) is not touched
        assert getattr(m, n) is f
    bad = g13_log(g13w, "c2_cand_Z1.json", drop_ids=["r1"], complete=False, incomplete_why=["x"])
    with pytest.raises(SystemExit):                                          # --final still refuses an incomplete log exactly as before
        m.g13_drop_ids(types.SimpleNamespace(final=True), c2io.C2InputLog(), [str(bad)], [])
    rep = {}
    m.write_outputs(a, rep, [], [])
    blk = rep[opt3.REPORT_KEY]
    assert written[m.OUT_MAN.name][opt3.REPORT_KEY] == blk and opt3.REPORT_KEY not in written["other.json"]
    assert orig_calls == [rep] and blk["ruling"]["id"] == "A68" and blk["report_only_targets"] == list(G.AC_TARGETS)
    assert blk["totals"]["ohsac_report_only_ids_sum"] == 3 and blk["drop_ids_field_unchanged"] is True
    assert blk["seed_quarantines"] == {"T27": {"binding": 2, "ohsac_report_only": 1}}
    assert "8.5" in " ".join(blk["not_changed"]) and "r1" not in json.dumps(blk)
    dry = {}
    m.dry_report = lambda rep_: rep_                                          # (dry_report wrapper was installed over the real one)


def test_nothing_in_the_option_edits_the_pinned_tools():
    """The pinned tools are patched in memory only: their files carry no mention of the option."""
    for n in ("g13_c2.py", "mix_c2.py", "c2_select.py"):
        assert "ac_report_only" not in (C2B / n).read_text(encoding="utf-8")


# ------------------------------------------------------------------------------------------------ the wrappers
def test_launch_without_the_flag_runs_the_original_untouched(monkeypatch):
    seen = {}
    monkeypatch.setattr(m, "main", lambda argv=None: seen.setdefault("mix", argv))
    monkeypatch.setattr(sel, "main", lambda argv=None: seen.setdefault("select", argv))
    monkeypatch.setattr(G, "main", lambda argv=None: seen.setdefault("g13", argv))
    for n in ("g13_drop_ids", "write_outputs", "dry_report"):
        monkeypatch.setattr(m, n, getattr(m, n))
    monkeypatch.setattr(m, "_opt3", False, raising=False)
    orig = (m.g13_drop_ids, m.write_outputs, m.dry_report, sel.drop_ids_of, G.derive_hits, G._record, G.withdraw_waivers)
    opt3.launch("mix", ["--dry-run", "--spend-to-date", "1"])
    opt3.launch("select", ["select", "--fam", "T28"])
    opt3.launch("g13", ["candidates", "--block", "T28"])
    assert seen == {"mix": ["--dry-run", "--spend-to-date", "1"], "select": ["select", "--fam", "T28"],
                    "g13": ["candidates", "--block", "T28"]}
    assert orig == (m.g13_drop_ids, m.write_outputs, m.dry_report, sel.drop_ids_of, G.derive_hits, G._record, G.withdraw_waivers)


def test_genfull_wrapper_delegates_and_patches_only_under_a_valid_ruling(monkeypatch, tmp_path):
    import gen_full_c2 as GEN
    seen = []
    monkeypatch.setattr(GEN, "main", lambda argv=None: seen.append(argv) or 0)
    monkeypatch.setattr(GEN, "g13_seed_templates", GEN.g13_seed_templates)
    monkeypatch.setattr(GEN, "_opt3_seed", False, raising=False)
    orig = GEN.g13_seed_templates
    assert opt3.launch("genfull", ["--fam", "T27"]) == 0 and GEN.g13_seed_templates is orig and seen == [["--fam", "T27"]]
    with pytest.raises(SystemExit):
        opt3.launch("genfull", ["--fam", "T27", "--ohsac-report-only", "A99"])           # no such ruling in the real PREREG_FINAL.md
    assert GEN.g13_seed_templates is orig and len(seen) == 1
    pre = tmp_path / "PREREG_FINAL.md"
    pre.write_text(PREREG)
    monkeypatch.setattr(c2io, "PREREG", pre)
    assert opt3.launch("genfull", ["--fam", "T27", "--ohsac-report-only", "A68"]) == 0
    assert GEN.g13_seed_templates is not orig and seen[-1] == ["--fam", "T27"]


def test_launch_refuses_an_unknown_ruling_id_and_patches_nothing(monkeypatch):
    called = []
    monkeypatch.setattr(m, "main", lambda argv=None: called.append(argv))
    monkeypatch.setattr(m, "_opt3", False, raising=False)
    orig = m.g13_drop_ids
    for rid in ("A64", "A38", "ZZ9"):                                       # none of these carries the marker in the real PREREG_FINAL.md
        with pytest.raises(SystemExit) as e:
            opt3.launch("mix", ["--ohsac-report-only", rid, "--dry-run"])
        assert "stays OFF" in str(e.value)
    assert called == [] and m.g13_drop_ids is orig and not getattr(m, "_opt3", False)


def test_launch_with_a_valid_ruling_installs_and_hands_over_the_rest(monkeypatch, tmp_path):
    pre = tmp_path / "PREREG_FINAL.md"
    pre.write_text(PREREG)
    monkeypatch.setattr(c2io, "PREREG", pre)
    seen = {}
    monkeypatch.setattr(m, "main", lambda argv=None: seen.setdefault("argv", argv))
    isolate(monkeypatch, m, ["g13_drop_ids", "write_outputs", "dry_report"])
    orig = m.g13_drop_ids
    opt3.launch("mix", ["--dry-run", "--ohsac-report-only", "A68", "--spend-to-date", "1"])
    assert seen["argv"] == ["--dry-run", "--spend-to-date", "1"] and m.g13_drop_ids is not orig and m._opt3 is True


# ------------------------------------------------------------------------------------------------ seed quarantines
def test_seed_quarantine_split_and_loader(tmp_path, monkeypatch):
    q = [{"template": "k1", "template_id": "t1", "file": "f.jsonl", "line": 1, "hits": {"ohsac_gtpl": ["gtpl8"]}},
         {"template": "k2", "template_id": "t2", "file": "f.jsonl", "line": 2, "hits": {"ohsac_hash": ["keyword"], "ohs4_hash": ["exact_full"]}},
         {"template": "k3", "template_id": "t3", "file": "f.jsonl", "line": 3, "hits": {"ohsac_hash": ["ngram10"], "ohsac_rows": ["tulu8"]}},
         {"template": "k4", "template_id": "t4", "file": "f.jsonl", "line": 4, "hits": {}}]
    b, ro = opt3.split_quarantine(q)
    assert [x["template_id"] for x in b] == ["t2", "t4"] and [x["template_id"] for x in ro] == ["t1", "t3"]
    d = opt3.binding_seed_log({"set": "c2_seed_T27", "quarantine": q, "quarantine_templates": 4})
    assert d["quarantine_templates"] == 2 and [x["template_id"] for x in d["ohsac_report_only_quarantine"]] == ["t1", "t3"]
    # gen_full_c2.g13_seed_templates: report-only templates are not removed
    fake = types.SimpleNamespace(G13_SEED_DIR=tmp_path)
    (tmp_path / "c2_seed_T27.json").write_text(json.dumps({"quarantine": q}))
    tpls = [{"template_id": t, "file": "f.jsonl", "line": i, "ids": [t], "resolved": True} for i, t in enumerate(("t1", "t2", "t3", "t4"), 1)]
    fake.g13_seed_templates = lambda fam, root=None: {"family": fam, "n_templates": 4, "templates": list(tpls)}
    use = opt3.UseLog()
    opt3.install_seed(fake, use)
    r = fake.g13_seed_templates("T27")
    assert [t["template_id"] for t in r["templates"]] == ["t2", "t4"] and r["n_templates"] == 2 and r["ohsac_report_only_templates"] == 2
    assert use.seed == {"T27": {"binding": 2, "ohsac_report_only": 2}}
    assert fake.g13_seed_templates("T99") is not None                       # no log file for T99: the original result as it is


def test_seed_split_cli_never_overwrites(tmp_path):
    src, out = tmp_path / "s.json", tmp_path / "o.json"
    src.write_text(json.dumps({"quarantine": [{"template_id": "t1", "hits": {"ohsac_hash": ["keyword"]}}]}))
    assert opt3.main(["seed-split", "--log", str(src), "--out", str(out)]) == 0
    assert json.loads(out.read_text())["quarantine"] == []
    with pytest.raises(SystemExit):
        opt3.main(["seed-split", "--log", str(src), "--out", str(out)])


def test_report_cli_counts_only(tmp_path, capsys):
    (tmp_path / "c2_cand_A.json").write_text(json.dumps(good_log()))
    (tmp_path / "c2_cand_B.json").write_text(json.dumps({"drop_ids": ["x"], "ohsac": {}}))
    (tmp_path / "acquick_c2_cand_A.json").write_text(json.dumps({"mode": "ohsac_only", "drop_ids": ["a", "b"], "ohsac": {}}))
    assert opt3.main(["report", "--log-dir", str(tmp_path)]) == 0
    out = [json.loads(x) for x in capsys.readouterr().out.splitlines()]
    by = {r["file"]: r for r in out if "file" in r}
    assert by["c2_cand_A.json"]["binding"] == 1 and by["c2_cand_A.json"]["ohsac_report_only"] == 2
    assert by["c2_cand_B.json"]["mode"] == "refused" and by["acquick_c2_cand_A.json"]["binding"] == 0


# ------------------------------------------------------------------------------------------------ the g13 capture, end to end
class FakeSide:
    """Stands in for AcSide: a text with ACHASH hits method `keyword` of ohsac_hash; everything else is complete."""

    def hash_compare(self, units):
        hits = {}
        for u in units:
            if any("ACHASH" in t for _f, t in u["texts"]):
                hits.setdefault("keyword", {})[u["key"]] = {"state"}
        return hits, {}, {}

    def completeness(self, units, cover):
        return True, []

    def record(self):
        return {"manifest_verified": True, "final": True, "union": {"status": "fake"}}


@pytest.fixture()
def capw(world, monkeypatch):
    """test_g13_c2's world with candidates for the split, a fake OHS-AC side, and a fake OHS-AC rows / G-TPL checker."""
    rows = [row(0, "Clean state about the canteen menu for next week and its prices."),
            row(1, "Ship today with " + SUITE_KEYWORD + " please, the client asked twice."),            # OHS-4 only
            row(2, "A row carrying ACHASH text only, in a harmless sentence about the weather today."),    # OHS-AC only (hash)
            row(3, "A row with ACROWS text for the fake AC rows checker, nothing else in it at all."),     # OHS-AC only (rows)
            row(4, "Both: " + SUITE_KEYWORD + " and ACHASH are in this one row of the candidates."),       # OHS-4 and OHS-AC
            row(5, "Partner row of unit c4, clean text only, with nothing to find anywhere.", call="c4")]
    world["cand"].write_text("".join(json.dumps(r) + "\n" for r in rows))
    orig = G.run_checker

    def run_checker(tool, flag, records, extra=None, **kw):
        if tool in (G.G13_OHSAC_TOOL, G.GTPL_AC_TOOL):
            ids = [r["id"] for r in records if "ACROWS" in (r.get("state") or r.get("text") or "")]
            return {"status": "scanned", "hit_ids": ids, "hit_ids_by_method": {"exact_seg": ids}}
        return orig(tool, flag, records, extra, **kw)

    monkeypatch.setattr(G, "run_checker", run_checker)
    monkeypatch.setattr(G, "ac_guard_files", lambda: [])
    monkeypatch.setattr(G, "_opt3_capture", False, raising=False)
    for n in ("derive_hits", "_record", "withdraw_waivers"):
        monkeypatch.setattr(G, n, getattr(G, n))
    return world


def no_time(o):
    if isinstance(o, dict):
        return {k: no_time(v) for k, v in o.items() if k not in ("wall_s", "unix")}
    if isinstance(o, list):
        return [no_time(v) for v in o]
    return o


def run_cap(w):
    return G.run("candidates", ["T98"], embed=False, side=False, tgs=w["tgs"] + G.c2_dev_targets(), exports=w["exports"], write=False,
                 prereg_text=A38, ohsac=True, ac_side=FakeSide())["c2_cand_T98"]


def test_the_g13_capture_splits_binding_from_ohsac_only_and_changes_nothing_else(capw):
    plain = run_cap(capw)
    assert opt3.CLASSES_KEY not in plain                                              # default: the record is exactly as before
    assert {"r1", "r2", "r3", "r4"} <= set(plain["drop_ids"]) and "r0" not in plain["drop_ids"]
    opt3.install_g13_capture(G, RULING)
    rec = run_cap(capw)
    cl = rec[opt3.CLASSES_KEY]
    assert cl["binding"] == ["r1", "r4", "r5"], cl                                    # r1 OHS-4 keyword; r4 + partner r5: OHS-4 AND OHS-AC
    assert set(cl["ohsac_report_only"]) == {"r2", "r3"} and not set(cl["binding"]) & set(cl["ohsac_report_only"])
    assert set(cl["binding"]) | set(cl["ohsac_report_only"]) == set(rec["drop_ids"])
    for k in plain:                                                                    # every other key of the record is the same
        if k not in ("wall_s", "unix"):
            assert no_time(rec[k]) == no_time(plain[k]), k
    assert set(rec) - set(plain) == {opt3.CLASSES_KEY}
    s = opt3.split_log(rec)
    assert s["mode"] == "by_class" and s["binding"] == set(cl["binding"]) and s["ruling"]["id"] == "A68"
    cap = cl["capture"]
    assert cap["set"] == "c2_cand_T98" and cap["run"] == "candidates" and cap["log_tool_sha256"] == rec["tool_sha256"]
    assert cap["ruling"] == {k: RULING[k] for k in ("id", "marker", "block_sha256", "prereg_sha256")} and len(cap["split_sha256"]) == 64
    json.dumps(rec)
    tampered = json.loads(json.dumps(rec))                                                # an id moved to the other class after the capture
    tampered[opt3.CLASSES_KEY]["binding"].remove("r1")
    tampered[opt3.CLASSES_KEY]["ohsac_report_only"].append("r1")
    with pytest.raises(opt3.SplitRefused) as e:
        opt3.split_log(tampered)
    assert "edited after the capture" in str(e.value)


def test_a_withdrawn_waiver_takes_the_split_back_with_it(capw, monkeypatch):
    """withdraw_waivers puts drop_ids back to the no-waiver hits; the split must follow, so drop_ids == binding + report-only still holds."""
    opt3.install_g13_capture(G, RULING)
    rec = run_cap(capw)
    unw = {"drop_ids": ["u1", "u2"], "drop_units": 2, "quarantine": [], "counts_by_target_and_method": {},
           opt3.CLASSES_KEY: {"binding": ["u1"], "ohsac_report_only": ["u2"], "units": {}, "capture": {"ac_targets": list(G.AC_TARGETS)}}}
    rec["a53"] = {"waived_units": 1}
    assert G.withdraw_waivers(rec, unw, ["x changed"]) is True
    assert rec[opt3.CLASSES_KEY]["binding"] == ["u1"] and set(rec["drop_ids"]) == {"u1", "u2"}
    rec["drop_ids"] = ["u1", "u2"]
    assert rec[opt3.CLASSES_KEY]["capture"]["split_sha256"] == opt3.split_digest(rec["set"], rec["run"], ["u1"], ["u2"], rec["tool_sha256"])
    rec2 = run_cap(capw)
    keep = dict(rec2[opt3.CLASSES_KEY])
    assert G.withdraw_waivers(rec2, None, []) is False and rec2[opt3.CLASSES_KEY] == keep


# ------------------------------------------------------------------------------------------------ A68 review fixes (17 Oct)
def test_a_split_captured_under_another_ruling_is_refused_in_select_and_mix(g13w, monkeypatch):
    other = {**RULING, "id": "A70", "block_sha256": "c" * 64}
    f = g13_log(g13w, "c2_cand_R1.json", drop_ids=["r1", "r2"], ohsac={"complete": True},
                drop_ids_by_class=sealed(["r1"], ["r2"], "c2_cand_R1", "candidates", None, ruling=other))
    isolate(monkeypatch, sel, ["drop_ids_of", "write_select"])
    opt3.install_select(sel, opt3.UseLog(RULING), RULING)
    with pytest.raises(opt3.SplitRefused) as e:
        sel.drop_ids_of(c2io.C2InputLog(), [str(f)])
    assert "A70" in str(e.value) and "A68" in str(e.value)
    same_id_other_block = {**RULING, "block_sha256": "d" * 64}                          # the ruling text changed after the capture
    with pytest.raises(opt3.SplitRefused):
        opt3.UseLog(same_id_other_block).add(f, json.loads(f.read_text()), opt3.split_log(json.loads(f.read_text())))


def test_the_selection_record_carries_the_option_block(g13w, monkeypatch):
    x, _y = ac_logs(g13w)
    isolate(monkeypatch, sel, ["drop_ids_of", "write_select"])
    written = {}
    monkeypatch.setattr(sel, "write_select", lambda fam, rec, extra: written.update({"fam": fam, "extra": extra}))
    use = opt3.UseLog(RULING)
    opt3.install_select(sel, use, RULING)
    sel.drop_ids_of(c2io.C2InputLog(), [str(x)])
    sel.write_select("T28", {}, {"candidates_sha256": "abc"})
    blk = written["extra"][opt3.REPORT_KEY]
    assert written["extra"]["candidates_sha256"] == "abc" and blk["ruling"]["id"] == "A68"
    assert blk["logs"][0]["captured_under"] == "A68" and blk["logs"][0]["ohsac_report_only"] == 2 and "r2" not in json.dumps(blk)
    assert blk["drop_ids_field_unchanged"] is True


def test_select_stamps_tell_strict_from_option3(tmp_path):
    (tmp_path / "select_T01.json").write_text(json.dumps({"x": 1}))
    (tmp_path / "select_T28.json").write_text(json.dumps({opt3.REPORT_KEY: {"ruling": {"id": "A68"}}}))
    (tmp_path / "select_T29.json").write_text(json.dumps({opt3.REPORT_KEY: {"ruling": {"id": "A70"}}}))
    (tmp_path / "select_T30.json").write_text("{")
    assert opt3.select_stamps(tmp_path, RULING) == {"T01": "strict", "T28": "option3 (A68)", "T29": "other ruling (A70)", "T30": "unreadable"}


def test_remove_sources_carries_the_block_over_or_refuses(tmp_path, monkeypatch):
    man = tmp_path / "c2_mix_manifest.json"
    man.write_text(json.dumps({"what": "m"}))
    with pytest.raises(SystemExit) as e:                                                # the written mix was made strict
        opt3.removal_block(man, RULING)
    assert "without the option" in str(e.value)
    blk = {"ruling": {"id": "A68"}, "logs": [{"file": "f"}], "totals": {"logs": 1}}
    man.write_text(json.dumps({"what": "m", opt3.REPORT_KEY: blk}))
    out = opt3.removal_block(man, RULING)
    assert out["logs"] == blk["logs"] and out["removal_pass"]["carried_over_unchanged"] is True
    with pytest.raises(SystemExit):
        opt3.removal_block(man, {**RULING, "id": "A70"})
    # the plain wrapper (no flag) refuses a removal on a mix written under the option; without the block it hands over untouched
    monkeypatch.setattr(m, "OUT_MAN", man)
    with pytest.raises(SystemExit) as e:
        opt3._refuse_plain_removal(m)
    assert "mix_c2_opt3.py" in str(e.value)
    man.write_text(json.dumps({"what": "m"}))
    opt3._refuse_plain_removal(m)
    seen = []
    monkeypatch.setattr(m, "main", lambda argv=None: seen.append(argv))
    opt3.launch("mix", ["--final", "--remove-sources", "x.json"])
    assert seen == [["--final", "--remove-sources", "x.json"]]


def test_the_mixer_writer_uses_the_carried_block_for_a_removal(monkeypatch, tmp_path):
    man = tmp_path / "c2_mix_manifest.json"
    blk = {"ruling": {"id": "A68"}, "logs": [{"file": "f"}], "totals": {"logs": 1}}
    man.write_text(json.dumps({"what": "m", opt3.REPORT_KEY: blk}))
    isolate(monkeypatch, m, ["g13_drop_ids", "write_outputs", "dry_report"])
    monkeypatch.setattr(m, "OUT_MAN", man)
    seen = {}
    monkeypatch.setattr(m, "write_outputs", lambda a, rep, rows, rels: seen.setdefault("rep", rep))
    opt3.install_mixer(m, RULING, opt3.UseLog(RULING), log_dir=None)
    rep = {}
    m.write_outputs(types.SimpleNamespace(remove_sources="x.json"), rep, [], [])
    assert rep[opt3.REPORT_KEY]["logs"] == blk["logs"] and "removal_pass" in rep[opt3.REPORT_KEY]


def test_genfull_report_names_the_templates_not_applied(tmp_path):
    q = [{"template": "k1", "template_id": "t1", "file": "f.jsonl", "line": 1, "hits": {"ohsac_gtpl": ["gtpl8"]}},
         {"template": "k2", "template_id": "t2", "file": "f.jsonl", "line": 2, "hits": {"ohs4_hash": ["exact_full"]}}]
    (tmp_path / "c2_seed_T27.json").write_text(json.dumps({"quarantine": q}))
    fake = types.SimpleNamespace(G13_SEED_DIR=tmp_path, g13_seed_templates=lambda fam, root=None: None,
                                 g13_report=lambda fam, ids, kit: {"source": "x", "clean": True} if ids else None)
    opt3.install_seed(fake, opt3.UseLog(RULING))
    assert fake.g13_report("T27", [], None) is None
    r = fake.g13_report("T27", ["i"], None)
    blk = r[opt3.REPORT_KEY]
    assert r["clean"] is True and blk["ruling"]["id"] == "A68" and [t["template_id"] for t in blk["templates_not_applied"]] == ["t1"]


def test_capture_plan_bounds_and_needs_capture(tmp_path):
    def cand(name, drop, rows, ac_units, counts, **kw):
        d = {"tool": "c2_build/g13_c2.py", "set": name, "run": "candidates", "complete": True, "rows": rows, "units": rows, "drop_units": len(drop),
             "drop_ids": drop, "ohsac": {"hit_units": ac_units}, "counts_by_target_and_method": counts} | kw
        (tmp_path / f"{name}.json").write_text(json.dumps(d))
    counts = {"ohs4_hash": {"keyword": {"units": 2, "rows": 2}}, "ohsac_hash": {"keyword": {"units": 5, "rows": 5}}}
    cand("c2_cand_A", ["a", "b", "c", "d", "e"], 8, 5, counts)
    (tmp_path / "acquick_c2_cand_A.json").write_text(json.dumps({"mode": "ohsac_only", "drop_ids": ["a", "b", "c", "d"]}))
    cand("c2_cand_B", ["a"], 3, 0, {"ohs4_hash": {"keyword": {"units": 1, "rows": 1}}}, **{"ohsac": None})
    cand("c2_cand_C", ["a", "b"], 3, 2, counts, **{opt3.CLASSES_KEY: sealed(["a"], ["b"], "c2_cand_C", "candidates", None)})
    plan = opt3.capture_plan(tmp_path)
    by = {r["set"]: r for r in plan["logs"]}
    a = by["c2_cand_A"]
    assert a["needs_capture"] is True and a["strict_drop_rows"] == 5
    assert a["binding_rows_at_least"] == 2 and a["report_only_rows_at_most"] == 3          # binding >= max(2 from OHS-4, 1 = e, not hit by OHS-AC)
    assert a["acquick"]["not_hit_by_ohsac_so_binding"] == 1 and a["rows_left_under_option3_at_least"] == 3
    assert by["c2_cand_B"]["needs_capture"] is False and by["c2_cand_B"]["has_ohsac_record"] is False
    assert by["c2_cand_C"]["needs_capture"] is False and by["c2_cand_C"]["valid_split_present"] is True
    assert plan["needs_capture"] == ["c2_cand_A.json"] and plan["must_produce"]["key"] == opt3.CLASSES_KEY
