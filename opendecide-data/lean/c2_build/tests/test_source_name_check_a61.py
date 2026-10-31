"""Tests for the A61 (f) fixes of meta_src/source_name_check.py (PREREG_FINAL.md Ruling A61; program fixes 1-3).

  1. HASHING UNCHANGED, identifier side: source_hashes() of every entry of five recorded inputs is identical under the old tool
     (_backup_a61_adopt/meta_src/source_name_check.py, sha 72fe203a...) and the new one; the source text of g13_c2's keyword_hashes, URL_RE,
     sha_hex, KW_STRIP is byte-identical in every g13_c2.py copy kept; source_name_check's load_hashes, HEX64, identifier_texts,
     source_hashes are byte-identical old vs new. These are hashing fixtures: the tests print booleans and counts only.
  2. HASHING UNCHANGED, export side: on fixture export folders that the test creates under tmp, the new compare set contains the old
     load_hashes set of every file the old tool read (plus the freeze export's keyword hashes).
  3. FOLD (PASS or HIT per source; a fold can only turn a PASS into a HIT), duplicate ids, exit 2 on a missing and on a MISMATCHing export
     (OHS-4, OHS-AC final, OHS-AC freeze), no verdict then, --exports ohs4 never binding.
No sealed folder is touched: every export is a fixture under tmp_path; run() is only ever called with build=<tmp_path>, and the module's pins
are monkeypatched to the fixtures' shas. Run from c2_build/:  ../../.venv/bin/python -B -m pytest -q tests/test_source_name_check_a61.py
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
import g13_c2  # noqa: E402  (imported first, so the old and new tool modules below find it in sys.modules)

ADOPT = C2B / "_backup_a61_adopt"
NEW_PATH = C2B / "meta_src" / "source_name_check.py"
OLD_PATH = ADOPT / "meta_src" / "source_name_check.py"
OLD_SHA = "72fe203a015aa4d5b292878dc871b21dcc4f0fdcab70e03fb142904b64fa1542"


def load_mod(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    before = list(sys.path)
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path[:] = before                       # the module inserts its own BUILD dir: never leave _backup_a61_adopt on sys.path
    return mod


snc = load_mod(NEW_PATH, "snc_new")
old = load_mod(OLD_PATH, "snc_old")


def sha_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


INPUTS = {
    "SOURCES_CANDIDATES": C2B / "meta_src/SOURCES_CANDIDATES.json",
    "SOURCES_SB5_85": C2B / "zed_orch/sb_blocks/SOURCES_SB5_85.json",
    "SOURCES_SB56_85": C2B / "zed_orch/sb_blocks/SOURCES_SB56_85.json",
    "SOURCES_DIKR_85": C2B / "zed_orch/di_train/DI-KR/SOURCES_DIKR_85.json",
    "DILANG_name_check_sources": C2B / "zed_orch/di_train/DI-LANG/provenance/name_check_sources.json",
}


# ---- the pre-fix tool is the pinned backup --------------------------------------------------------------------------------
def test_the_old_tool_is_the_pinned_backup():
    assert sha_file(OLD_PATH) == OLD_SHA


def test_pins_equal_g13_c2s_pins():
    assert snc.OHS4_MANIFEST_SHA256 == g13_c2.SEALED_HASHES_MANIFEST_SHA256
    assert snc.OHS4_FREEZE_SHA256 == g13_c2.OHS4_FREEZE_SHA256
    assert snc.OHSAC_FINAL_MANIFEST_SHA256 == "fadec66fdb3824ca3e81096c65b15d5e8cac7998a05fc964d0ce1b4fdb36cd9b"
    assert snc.OHSAC_FREEZE_MANIFEST_SHA256 == "27808b0ccbaf69aae058745ef0e80db6f5b692648198f26161bf749c3f1c3f6e"
    assert all(len(x) == 64 for x in (snc.OHS4_MANIFEST_SHA256, snc.OHS4_FREEZE_SHA256, snc.OHSAC_FINAL_MANIFEST_SHA256,
                                      snc.OHSAC_FREEZE_MANIFEST_SHA256))


# ---- (a) identifier side: source_hashes() identical on every entry of the five recorded inputs --------------------------------
@pytest.mark.parametrize("name", sorted(INPUTS))
def test_source_hashes_identical_old_and_new_on_every_entry(name):
    p = INPUTS[name]
    assert p.is_file(), "recorded hashing fixture missing"
    srcs = json.loads(p.read_text(encoding="utf-8"))["sources"]
    same = [snc.source_hashes(s) == old.source_hashes(s) for s in srcs]
    texts_same = [snc.identifier_texts(s) == old.identifier_texts(s) for s in srcs]
    assert len(srcs) > 0 and all(same) and all(texts_same)
    print(f"{name}: entries {len(srcs)}, source_hashes identical {sum(same)}/{len(srcs)}")      # booleans / counts only


# ---- (b) byte-identical source text, checked by AST segment -------------------------------------------------------------------
def segments(path: Path, names) -> dict:
    src = Path(path).read_text(encoding="utf-8")
    out = {}
    for node in ast.parse(src).body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in names:
            out[node.name] = ast.get_source_segment(src, node)
        elif isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in names:
            out[node.targets[0].id] = ast.get_source_segment(src, node)
    return out


G13_NAMES = ("keyword_hashes", "URL_RE", "sha_hex", "KW_STRIP")
G13_COPIES = {                                           # sha256 -> path (the shas are asserted, then the segments compared)
    "904d914c": C2B / "_backup_refresh/g13_c2.py",
    "213634d7": C2B / "_backup_a61/g13_c2.py",
    "32256eaa": ADOPT / "g13_c2.32256eaa.py",
    "window-start": ADOPT / "g13_c2.py",
    "live (the g13_c2.py of the step-9 run)": C2B / "g13_c2.py",
}


def test_g13_copies_have_their_logged_shas():
    assert sha_file(G13_COPIES["904d914c"]).startswith("904d914c477db958")
    assert sha_file(G13_COPIES["213634d7"]) == "213634d77c868e28a6130cc13fb2910c032f88d1d37811c829bd5edf3db8853c"
    assert sha_file(G13_COPIES["32256eaa"]) == "32256eaa2328c5029b02b2835ff00cb97bb34cd3abf748db0d6631e680b75776"


def test_g13_hashing_helpers_byte_identical_in_every_copy():
    ref = segments(G13_COPIES["213634d7"], G13_NAMES)
    assert set(ref) == set(G13_NAMES)
    res = {k: segments(p, G13_NAMES) == ref for k, p in G13_COPIES.items()}
    assert all(res.values()), res
    print(f"g13_c2 hashing helpers byte-identical in {sum(res.values())}/{len(res)} copies")


def test_g13_hashing_helpers_behave_identically_in_every_copy():
    """Executes the four segments of each copy and compares outputs on identifier texts (a stronger check than the text compare)."""
    import re
    from urllib.parse import urlsplit
    samples = ["Wikipedia", "Hugging Face datasets", "https://www.example.org/a/b?c=d", "uci 293, 'Title': (Z) {a} [b]", "", "x  y\tz\n w",
               "ÉCOLE normale — dataset v1.2"]
    for p in {str(v): v for v in G13_COPIES.values()}.values():
        seg = segments(p, G13_NAMES)
        ns = {"re": re, "hashlib": hashlib, "urlsplit": urlsplit}
        exec("\n".join(seg[n] for n in ("KW_STRIP", "URL_RE", "sha_hex", "keyword_hashes")), ns)
        for t in samples:
            assert ns["keyword_hashes"](t) == g13_c2.keyword_hashes(t)
            assert ns["sha_hex"](t) == g13_c2.sha_hex(t)


def test_source_name_check_hashing_helpers_byte_identical_old_vs_new():
    names = ("load_hashes", "HEX64", "identifier_texts", "source_hashes")
    o, n = segments(OLD_PATH, names), segments(NEW_PATH, names)
    assert set(o) == set(names) == set(n)
    same = {k: o[k] == n[k] for k in names}
    assert all(same.values()), same


# ---- (c) export side: containment on fixture export folders -------------------------------------------------------------------
FREEZE_SHA = snc.OHSAC_FREEZE_MANIFEST_SHA256


def kw_lines(tag: str) -> list:
    """Keyword lines of several shapes: under "hash" and other keys, several kinds, non-hash strings, blank and bad lines."""
    h = lambda s: g13_c2.sha_hex(f"{tag} {s}")      # noqa: E731
    return [json.dumps({"kind": "keyword", "hash": h("a")}), json.dumps({"kind": "keyword_url", "hash": h("b")}),
            json.dumps({"h": h("c"), "note": "not a hash", "n": 3}), json.dumps({"kind": "x", "sha256": h("d"), "hash": "zz" + h("e")[2:]}),
            json.dumps(h("f")), json.dumps([h("g")]), json.dumps({"kind": "keyword", "hash": h("A").upper()}),   # upper-case: not a hash
            "", "   ", "{not json", json.dumps({"hash": h("a")[:63]}), json.dumps({"hash": 12345}), json.dumps({"hash": None})]


class Build:
    """A fixture build dir with the three export folders; every pin of the module is monkeypatched to it."""

    def __init__(self, root: Path, mp):
        self.root = root
        self.ohs4, self.ac, self.union = root / "sealed_hashes", root / "sealed_hashes_ac", root / "sealed_hashes_ac_union"
        for d in (self.ohs4, self.ac, self.union):
            d.mkdir(parents=True)
        self.mp = mp
        self.write_ohs4(kw_lines("ohs4"))
        self.write_final(kw_lines("final"))
        self.write_union("freeze_subset_of_final")
        self.pin()

    # -- writers (each rewrites the manifest with the file's current sha256)
    def write_ohs4(self, lines, freeze=None):
        (self.ohs4 / snc.KW).write_text("\n".join(lines) + "\n", encoding="utf-8")
        (self.ohs4 / "MANIFEST.json").write_text(json.dumps({
            "freeze_manifest_sha256": freeze or snc.OHS4_FREEZE_SHA256,
            "files": {snc.KW: {"sha256": sha_file(self.ohs4 / snc.KW)}}}), encoding="utf-8")

    def write_final(self, lines):
        (self.ac / snc.KW).write_text("\n".join(lines) + "\n", encoding="utf-8")
        (self.ac / "MANIFEST.json").write_text(json.dumps({"sha256": {snc.KW: sha_file(self.ac / snc.KW)}, "stage": "final"}), encoding="utf-8")

    def write_prelim(self, lines):
        (self.ac / snc.PRELIM).write_text("\n".join(lines) + "\n", encoding="utf-8")

    def write_union(self, status, lines=None, counts=None, freeze=None, final=None, with_sha=True):
        rec = {"status": status, "freeze_manifest_sha256": freeze or FREEZE_SHA,
               "counts": {"keyword_hashes.jsonl:keyword": 0, "ngrams10_sha256.npy": 0} if counts is None else counts}
        if final is not None:
            rec["final_manifest_sha256"] = final
        if status == "union_built":
            (self.union / snc.KW).write_text("\n".join(lines or []) + "\n", encoding="utf-8")
            rec["sha256"] = {snc.KW: sha_file(self.union / snc.KW)} if with_sha else {}
        (self.union / "RECORD.json").write_text(json.dumps(rec), encoding="utf-8")

    def pin(self):
        for attr, p in (("OHS4_MANIFEST_SHA256", self.ohs4 / "MANIFEST.json"), ("OHSAC_FINAL_MANIFEST_SHA256", self.ac / "MANIFEST.json")):
            if p.exists():
                self.mp.setattr(snc, attr, sha_file(p))

    def input_file(self, entries, name="in.json") -> Path:
        p = self.root / name
        p.write_text(json.dumps({"sources": entries}), encoding="utf-8")
        return p

    def run(self, entries, *flags):
        return snc.run(["--file", str(self.input_file(entries)), *flags], build=self.root)


@pytest.fixture
def bld(tmp_path, monkeypatch):
    return Build(tmp_path / "build", monkeypatch)


def entry(i, name, **kw):
    return {"id": i, "role": "metadata", "name": name, "publisher": "", "host": "", "upstream_id": "", "licence_url": "", "dataset_url": "", **kw}


def test_new_compare_set_contains_the_old_one_for_every_file(bld):
    bld.write_prelim(kw_lines("prelim"))
    bld.write_union("union_built", lines=kw_lines("freeze"))
    problems, new = snc.compare_set(bld.root, "all")
    assert problems == []
    olds = {f: old.load_hashes(p) for f, p in (("ohs4", bld.ohs4 / snc.KW), ("final", bld.ac / snc.KW), ("prelim", bld.ac / snc.PRELIM))}
    res = {k: v <= new for k, v in olds.items()}
    assert all(res.values()) and all(len(v) > 0 for v in olds.values())
    freeze = old.load_hashes(bld.union / snc.KW)
    assert freeze and freeze <= new and freeze.isdisjoint(set().union(*olds.values()))        # the freeze export ADDS hashes
    assert new == set().union(*olds.values()) | freeze                                         # nothing else enters
    # the same load_hashes semantics on the odd lines: only 64-hex lowercase strings, under any key, any JSON shape
    got = old.load_hashes(bld.ohs4 / snc.KW)
    assert g13_c2.sha_hex("ohs4 a") in got and g13_c2.sha_hex("ohs4 f") in got and g13_c2.sha_hex("ohs4 c") in got
    assert snc.load_hashes(bld.ohs4 / snc.KW) == got
    print(f"containment: ohs4 {len(olds['ohs4'])}, final {len(olds['final'])}, prelim {len(olds['prelim'])}, freeze {len(freeze)}, new {len(new)}")


def test_ohs4_only_compare_set_is_the_ohs4_file_alone(bld):
    bld.write_prelim(kw_lines("prelim"))
    problems, s = snc.compare_set(bld.root, "ohs4")
    assert problems == [] and s == old.load_hashes(bld.ohs4 / snc.KW)


def test_prelim_file_is_still_read_when_present_and_optional_when_absent(bld):
    h = g13_c2.sha_hex("only in the preliminary file")
    src = entry("P1", "only in the preliminary file")
    assert bld.run([src]) == (0, ["P1 PASS"])
    bld.write_prelim([json.dumps({"kw": h})])
    assert bld.run([src]) == (0, ["P1 HIT"])
    assert bld.run([src], "--exports", "ohs4") == (0, ["P1 PASS-NONBINDING"])          # not read under ohs4


def test_freeze_keyword_hashes_enter_from_the_union_file_or_from_the_final_export(bld):
    only_freeze = entry("F1", "freeze only identifier")
    only_final = entry("F2", "final only identifier")
    bld.write_final(kw_lines("final") + [json.dumps({"kind": "keyword", "hash": g13_c2.sha_hex("final only identifier")})])
    bld.pin()
    bld.write_union("freeze_subset_of_final")                                         # 0 freeze hashes outside the final export
    assert bld.run([only_freeze, only_final]) == (0, ["F1 PASS", "F2 HIT"])
    bld.write_union("union_built", lines=[json.dumps({"kind": "keyword", "hash": g13_c2.sha_hex("freeze only identifier")})])
    assert bld.run([only_freeze, only_final]) == (0, ["F1 HIT", "F2 HIT"])


# ---- (d) the fold -------------------------------------------------------------------------------------------------------------
def test_fold_one_line_per_source_and_a_hit_entry_makes_the_source_a_hit(bld):
    hit = g13_c2.sha_hex("sealed dataset name")
    bld.write_final(kw_lines("final") + [json.dumps({"kind": "keyword", "hash": hit})])
    bld.pin()
    es = [entry("md_x", "clean one"), entry("md_x#2", "sealed dataset name"), entry("md_x#3", "clean three"),
          entry("md_y", "clean y"), entry("md_y#1", "clean y again"),
          entry("md_z", "sealed dataset name"), entry("md_z", "clean z duplicate id"),            # duplicate ids fold too
          entry("md_w", "clean w"), entry("md_w", "clean w again")]
    code, lines = bld.run(es)
    assert code == 0 and lines == ["md_x HIT", "md_y PASS", "md_z HIT", "md_w PASS"]            # first-appearance order, one line per source
    assert bld.run(list(reversed(es)))[1] == ["md_w PASS", "md_z HIT", "md_y PASS", "md_x HIT"]   # entry order inside a source does not matter


def test_a_fold_can_only_turn_a_pass_into_a_hit_never_the_reverse(bld):
    """Entrywise (the pre-fix tool's rule, one verdict per entry) vs per source: every source with a HIT entry is a HIT; a PASS source has no HIT entry."""
    pool = ["alpha corpus", "beta corpus", "gamma corpus", "delta corpus", "epsilon corpus"]
    bld.write_final(kw_lines("final") + [json.dumps({"kind": "keyword", "hash": g13_c2.sha_hex(pool[1])}),
                                          json.dumps({"kind": "keyword", "hash": g13_c2.sha_hex(pool[3])})])
    bld.pin()
    es = [entry(f"s{i % 3}" + ("" if i % 2 else f"#{i}"), pool[i % 5]) for i in range(12)] + [entry("s9#1", pool[2]), entry("s9", pool[4])]
    _, bad = snc.compare_set(bld.root, "all")
    per_entry = {}
    for e in es:
        per_entry.setdefault(e["id"].split("#")[0], []).append(bool(old.source_hashes(e) & bad))
    code, lines = bld.run(es)
    got = dict(x.split(" ") for x in lines)
    assert code == 0 and set(got) == set(per_entry) and len(lines) == len(per_entry)
    for sid, flags in per_entry.items():
        assert (got[sid] == "HIT") == any(flags)
        if any(flags) is False:
            assert got[sid] == "PASS"
    assert any(v == "HIT" for v in got.values()) and any(v == "PASS" for v in got.values())


def test_role_filter_is_kept(bld):
    es = [entry("a", "clean a", role="g_proxy"), entry("b", "clean b", role="metadata")]
    assert bld.run(es, "--role", "metadata") == (0, ["b PASS"])
    assert bld.run(es, "--role", "g_proxy") == (0, ["a PASS"])


def test_output_is_only_id_pass_or_hit_lines(bld):
    code, lines = bld.run([entry("a", "clean a"), entry("a#1", "x")])
    assert code == 0 and all(len(x.split(" ")) == 2 and x.split(" ")[1] in ("PASS", "HIT") for x in lines)


# ---- (e) export integrity: missing / MISMATCH -> only that line, no verdict, exit 2 -------------------------------------------
ENT = [entry("a", "clean a")]


def test_a_complete_verified_set_gives_exit_0(bld):
    assert bld.run(ENT) == (0, ["a PASS"])


@pytest.mark.parametrize("what", ["manifest", "file", "dir"])
def test_ohs4_missing(bld, what):
    {"manifest": lambda: (bld.ohs4 / "MANIFEST.json").unlink(), "file": lambda: (bld.ohs4 / snc.KW).unlink(),
     "dir": lambda: __import__("shutil").rmtree(bld.ohs4)}[what]()
    assert bld.run(ENT) == (2, ["OHS-4 export missing"])


def test_ohs4_manifest_sha_not_the_pin(bld):
    (bld.ohs4 / "MANIFEST.json").write_text((bld.ohs4 / "MANIFEST.json").read_text() + " ")
    assert bld.run(ENT) == (2, ["OHS-4 export MISMATCH"])


def test_ohs4_keyword_file_changed_after_the_manifest(bld):
    (bld.ohs4 / snc.KW).write_text("\n".join(kw_lines("tampered")) + "\n")
    assert bld.run(ENT) == (2, ["OHS-4 export MISMATCH"])


def test_ohs4_manifest_naming_another_freeze(bld):
    bld.write_ohs4(kw_lines("ohs4"), freeze="0" * 64)
    bld.pin()
    assert bld.run(ENT) == (2, ["OHS-4 export MISMATCH"])


@pytest.mark.parametrize("what", ["manifest", "file"])
def test_ohsac_final_missing(bld, what):
    (bld.ac / ("MANIFEST.json" if what == "manifest" else snc.KW)).unlink()
    assert bld.run(ENT) == (2, ["OHS-AC final export missing"])


def test_ohsac_final_manifest_not_the_pin_and_file_tampered(bld):
    (bld.ac / "MANIFEST.json").write_text((bld.ac / "MANIFEST.json").read_text() + " ")
    assert bld.run(ENT) == (2, ["OHS-AC final export MISMATCH"])
    bld.write_final(kw_lines("final"))
    bld.pin()
    assert bld.run(ENT)[0] == 0
    (bld.ac / snc.KW).write_text("\n".join(kw_lines("tampered")) + "\n")
    assert bld.run(ENT) == (2, ["OHS-AC final export MISMATCH"])


def test_ohsac_final_manifest_without_the_keyword_entry(bld):
    (bld.ac / "MANIFEST.json").write_text(json.dumps({"sha256": {}}))
    bld.pin()
    assert bld.run(ENT) == (2, ["OHS-AC final export MISMATCH"])


def test_freeze_record_missing_or_lost(bld):
    (bld.union / "RECORD.json").unlink()
    assert bld.run(ENT) == (2, ["OHS-AC freeze export missing"])
    bld.write_union("lost")
    assert bld.run(ENT) == (2, ["OHS-AC freeze export missing"])
    __import__("shutil").rmtree(bld.union)
    assert bld.run(ENT) == (2, ["OHS-AC freeze export missing"])


@pytest.mark.parametrize("kw", [dict(freeze="1" * 64), dict(final="2" * 64), dict(counts={"k": 1}), dict(counts={}), dict(counts={"k": True}),
                                dict(counts={"k": -1})])
def test_freeze_record_mismatch_cases_for_freeze_subset_of_final(bld, kw):
    bld.write_union("freeze_subset_of_final", **kw)
    assert bld.run(ENT) == (2, ["OHS-AC freeze export MISMATCH"])


def test_freeze_record_with_another_status_or_unreadable(bld):
    (bld.union / "RECORD.json").write_text(json.dumps({"status": "something", "freeze_manifest_sha256": FREEZE_SHA, "counts": {"k": 0}}))
    assert bld.run(ENT) == (2, ["OHS-AC freeze export MISMATCH"])
    (bld.union / "RECORD.json").write_text("{not json")
    assert bld.run(ENT) == (2, ["OHS-AC freeze export MISMATCH"])
    (bld.union / "RECORD.json").write_text("[]")
    assert bld.run(ENT) == (2, ["OHS-AC freeze export MISMATCH"])


def test_freeze_record_union_built_verified_against_the_recorded_sha(bld):
    bld.write_union("union_built", lines=kw_lines("freeze"))
    assert bld.run(ENT) == (0, ["a PASS"])
    bld.write_union("union_built", lines=kw_lines("freeze"))
    (bld.union / snc.KW).write_text("\n".join(kw_lines("tampered")) + "\n")
    assert bld.run(ENT) == (2, ["OHS-AC freeze export MISMATCH"])
    bld.write_union("union_built", lines=kw_lines("freeze"), with_sha=False)
    assert bld.run(ENT) == (2, ["OHS-AC freeze export MISMATCH"])
    bld.write_union("union_built", lines=kw_lines("freeze"))
    (bld.union / snc.KW).unlink()
    assert bld.run(ENT) == (2, ["OHS-AC freeze export missing"])


def test_freeze_record_naming_the_fixture_final_manifest_is_accepted(bld):
    bld.write_union("freeze_subset_of_final", final=snc.OHSAC_FINAL_MANIFEST_SHA256)
    assert bld.run(ENT) == (0, ["a PASS"])


def test_every_failing_export_is_named_and_nothing_else_is_printed(bld):
    (bld.ohs4 / "MANIFEST.json").unlink()
    (bld.ac / snc.KW).write_text("x\n")
    code, lines = bld.run([entry("a", "clean a"), entry("b", "clean b")])
    assert code == 2 and lines == ["OHS-4 export missing", "OHS-AC final export MISMATCH"]      # no "<id> PASS|HIT" line at all


def test_integrity_is_checked_before_the_input_file_is_read(bld):
    (bld.ohs4 / "MANIFEST.json").unlink()
    code, lines = snc.run(["--file", str(bld.root / "does_not_exist.json")], build=bld.root)
    assert (code, lines) == (2, ["OHS-4 export missing"])


def test_ohs4_mode_checks_only_ohs4_and_is_never_binding(bld):
    (bld.ac / "MANIFEST.json").unlink()
    (bld.union / "RECORD.json").unlink()
    assert bld.run([entry("a", "clean a")], "--exports", "ohs4") == (0, ["a PASS-NONBINDING"])
    assert bld.run([entry("a", "clean a")]) == (2, ["OHS-AC final export missing", "OHS-AC freeze export missing"])
    bld.write_ohs4(kw_lines("ohs4") + [json.dumps({"kind": "keyword", "hash": g13_c2.sha_hex("hit name")})])
    bld.pin()
    assert bld.run([entry("a", "hit name")], "--exports", "ohs4") == (0, ["a HIT"])
    assert all(x.split(" ")[1] not in ("PASS",) for x in bld.run([entry("c", "clean c")], "--exports", "ohs4")[1])


def test_any_other_exception_prints_nothing_and_exits_2(bld, tmp_path):
    assert snc.run(["--file", str(tmp_path / "missing.json")], build=bld.root) == (2, [])
    bad = tmp_path / "bad.json"
    bad.write_text("{not json")
    assert snc.run(["--file", str(bad)], build=bld.root) == (2, [])
    bad.write_text(json.dumps({"sources": [{"role": "metadata", "name": "no id"}]}))
    assert snc.run(["--file", str(bad)], build=bld.root) == (2, [])
    bad.write_text(json.dumps({"sources": [{"id": 5, "role": "metadata"}]}))
    assert snc.run(["--file", str(bad)], build=bld.root) == (2, [])


def test_main_prints_the_lines_and_exits_with_the_code(bld, capsys, monkeypatch):
    monkeypatch.setattr(snc, "run", lambda argv=None, build=None: (2, ["OHS-4 export missing"]))
    with pytest.raises(SystemExit) as e:
        snc.main()
    assert e.value.code == 2 and capsys.readouterr().out == "OHS-4 export missing\n"
    monkeypatch.setattr(snc, "run", lambda argv=None, build=None: (0, ["a PASS", "b HIT"]))
    with pytest.raises(SystemExit) as e:
        snc.main()
    assert e.value.code == 0 and capsys.readouterr().out == "a PASS\nb HIT\n"
