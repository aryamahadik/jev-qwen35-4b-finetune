"""Tests for g13_di/di_register.py (fetch-src, finalize, export) on SYNTHETIC files under pytest's tmp_path: nothing under
bench/external_quarantine/ is read, written or stat-ed, nothing is fetched from the network (R.fetch is replaced), and the real
g13_di/ files are not touched (the module paths are redirected). Run from lean/:
  ../.venv/bin/python -B -m pytest -q c2_build/tests/test_di_register.py
"""
from __future__ import annotations

import gzip
import hashlib
import io
import json
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2B = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(C2B))
sys.path.insert(0, str(C2B / "g13_di"))
import di_g13 as D  # noqa: E402
import di_register as R  # noqa: E402

g = D.g


def req(cid, i, state="A synthetic state about harbours and tides number %d", instr="Decide which option the rule selects here", crit=None):
    return {"id": f"c{cid}-{i}", "state": state % i if "%d" in state else state,
            "questions": {"q": {"type": "choice", "instructions": instr, "criteria": crit or {"A": "first choice", "B": "second choice"}}},
            "expected": {"q": "A"}, "_evaluation": {"run_id": f"{cid}:{i}", "catalog_id": cid, "dataset": f"B{cid}"}}


def write_gz(p: Path, rows) -> str:
    p.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(p, "wb", compresslevel=1) as f:
        for r in rows:
            f.write((json.dumps(r) + "\n").encode())
    with gzip.open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


@pytest.fixture()
def env(tmp_path, monkeypatch):
    di = tmp_path / "g13_di"
    di.mkdir()
    root = tmp_path / "repo"
    monkeypatch.setattr(D, "DI_DIR", di)
    monkeypatch.setattr(D, "PINS", di / "di_pins.json")
    monkeypatch.setattr(D, "NEVER_TRAIN", di / "di_never_train.json")
    monkeypatch.setattr(D, "EXPORT_MANIFEST", di / "MANIFEST.json")
    monkeypatch.setattr(R, "HERE", di)
    return di, root


def kit_pin(unc: dict, extra_bench=()):
    bench = [{"catalog_id": 1, "dataset": "B1", "requests": 3}, {"catalog_id": 2, "dataset": "B2", "requests": 9999},
             {"catalog_id": 45, "dataset": "HLE", "requests": 513}, *extra_bench]
    return {"repo": "https://github.com/apolinario/decision-index", "commit": "c" * 40, "edition": "release-v3",
            "files": {R.MANIFEST_PATH: {"sha256": "a" * 64}, R.SUITE_MD: {"sha256": "b" * 64}},
            "benchmarks": bench, "added": [{"catalog_id": 57, "dataset": "MMLU-Pro", "requests": 2}],
            "manifest_files": {n: {"uncompressed_sha256": s} for n, s in unc.items()}}


def build_di03(root: Path, drop=()):
    """Three synthetic DI files: B1 x3 and B2 x2 (catalog 2: the lab's v2 count is 1,328, so the rebuild is short), MMLU-Pro x2, GSM8K-like x1."""
    files = {}
    rows = [req(1, i) for i in range(3)] + [req(2, i) for i in range(2)]
    files[D.DI03_FILES[0]] = rows
    files[D.DI03_FILES[1]] = [req(57, 0, instr="Pick the correct option for the question above now"), req(57, 1)]
    files[D.DI03_FILES[2]] = [req(30, 0)]
    unc = {}
    for rel, rr in files.items():
        if Path(rel).name in drop:
            continue
        unc[Path(rel).name] = write_gz(root / rel, rr)
    return unc


def test_finalize_reports_rebuilt_counts_gaps_and_the_hle_rule(env):
    di, root = env
    unc = build_di03(root)
    (di / "kit_pin.json").write_text(json.dumps(kit_pin(unc)))
    pins = R.cmd_finalize(type("A", (), {"root": str(root)})())
    p = pins["di03_public"]
    assert set(p["files"]) == set(D.DI03_FILES) and all(f["rows"] > 0 and len(f["sha256"]) == 64 for f in p["files"].values())
    assert p["build"] == "published" and all(p["byte_identical"].values())            # the manifest says these ARE the unc hashes
    assert p["per_benchmark"]["2"] == {"dataset": "B2", "expected": 1328, "rebuilt": 2}  # V2_COUNTS: ToolRet-like catalog 2 is 1,328 in the cut
    assert "B2: 2 of 1328 requests rebuilt" in p["gaps"] and D.HLE_GAP in p["gaps"]
    assert p["complete"] is False                                                     # a gap other than HLE: incomplete (A61 e 2)
    assert D.gap_for("di03_public", pins, "> **Ruling A61 (x)**\n> A61-HLE\n").startswith("di03_public: incomplete (B2: 2 of 1328")
    # a rebuild whose only gap is HLE is complete, and the HLE gap needs the ruling tag
    unc = build_di03(root)
    ok = kit_pin(unc)
    ok["benchmarks"] = [b for b in ok["benchmarks"] if b["catalog_id"] != 2] + [{"catalog_id": 30, "dataset": "GSM8K", "requests": 1}]
    (di / "kit_pin.json").write_text(json.dumps(ok))
    p2 = R.cmd_finalize(type("A", (), {"root": str(root)})())["di03_public"]
    assert p2["gaps"] == [D.HLE_GAP] and p2["complete"] is True
    assert "A61-HLE" in D.gap_for("di03_public", D.load_pins(), "no ruling") and D.gap_for("di03_public", D.load_pins(), "> **Ruling A61 (x)**\n> A61-HLE\n") is None
    # not byte-identical -> "rebuilt"
    ok["manifest_files"][Path(D.DI03_FILES[0]).name]["uncompressed_sha256"] = "0" * 64
    (di / "kit_pin.json").write_text(json.dumps(ok))
    p3 = R.cmd_finalize(type("A", (), {"root": str(root)})())["di03_public"]
    assert p3["build"] == "rebuilt" and p3["byte_identical"][Path(D.DI03_FILES[0]).name] is False and p3["complete"] is True


def test_finalize_with_a_missing_file_or_nothing_rebuilt_is_incomplete(env):
    di, root = env
    unc = build_di03(root, drop=("gsm8k-rows.jsonl.gz",))
    (di / "kit_pin.json").write_text(json.dumps(kit_pin(unc)))
    p = R.cmd_finalize(type("A", (), {"root": str(root)})())["di03_public"]
    assert not p["complete"] and any("gsm8k-rows.jsonl.gz" in x for x in p["gaps"])
    empty = R.cmd_finalize(type("A", (), {"root": str(root / "nowhere")})())["di03_public"]
    assert empty["complete"] is False and empty["files"] == {} and empty["gaps"] == ["not rebuilt yet: none of the three DI files exists"]
    assert D.gap_for("di_src_splits", D.load_pins()) is not None                       # no src splits fetched: incomplete too


def test_finalize_writes_the_never_train_fragment_with_paths_and_hashes(env):
    di, root = env
    unc = build_di03(root)
    (di / "kit_pin.json").write_text(json.dumps(kit_pin(unc)))
    R.cmd_finalize(type("A", (), {"root": str(root)})())
    nt = json.loads(D.NEVER_TRAIN.read_text())
    assert {Path(f["path"]).name for f in nt["files"]} == {Path(f).name for f in D.DI03_FILES} and set(nt["names"]) == set(D.TARGETS)
    assert all(f["path"].startswith(str(root)) and len(f["sha256"]) == 64 for f in nt["files"])
    import mix_c2 as m
    never = m.merge_di_never_train({"paths": set(), "sha256": set(), "names": set()}, D.NEVER_TRAIN)
    assert len(never["paths"]) == 3 and len(never["sha256"]) == 3 and set(D.TARGETS) <= never["names"]


def test_export_builds_the_hashed_wording_and_structure_sets_and_di_exports_loads_them(env):
    di, root = env
    unc = build_di03(root)
    (di / "kit_pin.json").write_text(json.dumps(kit_pin(unc)))
    R.cmd_finalize(type("A", (), {"root": str(root)})())
    (di / "record_ids.json").write_text(json.dumps({"gsm8k_question_sha256": [], "hover_claim_sha256": [], "hover_uid": [], "hover_group": [],
                                                    "isarcasm_text_sha256": []}))
    man = R.cmd_export(type("A", (), {"root": str(root)})())
    assert man["requests_read"] == 8 and man["counts"]["structure_g13"] >= 1 and man["counts"]["wording8"] >= 1
    pins = D.load_pins()
    ex = D.DiExports(di, pins)                                                         # verifies the manifest and the pinned derivation
    from test_g13_c2_di import unit
    hit = unit(0, instructions="Please pick the correct option for the question above now ok")
    clean = unit(1, instructions="Something wholly unrelated to the decision index wording at all today")
    hits, _ = D.di_hits([hit, clean], ex)
    assert set(hits["di03_public"]["wording8"]) == {"c0"}
    st = unit(2, state="A synthetic state about harbours and tides number 1", options=["first choice", "second choice"])
    assert "c2" in D.di_hits([st], ex)[0]["di03_public"]["structure"]
    # a rebuild after the export makes the export stale (derived_from no longer matches the pins)
    root2 = root.parent / "repo2"
    unc2 = {}
    for rel, rr in {D.DI03_FILES[0]: [req(1, 99)], D.DI03_FILES[1]: [req(57, 5)], D.DI03_FILES[2]: [req(30, 5)]}.items():
        unc2[Path(rel).name] = write_gz(root2 / rel, rr)
    R.cmd_finalize(type("A", (), {"root": str(root2)})())
    with pytest.raises(D.DiError, match="other DI files"):
        D.DiExports(di, D.load_pins())


def test_fetch_src_writes_the_full_splits_and_hashed_ids_and_checks_the_row_counts(env, monkeypatch):
    di, root = env
    import pyarrow as pa
    import pyarrow.parquet as pq
    gsm = [{"question": f"Tom buys {i} apples and then {i + 1} pears at the market so how many fruits", "answer": f"{i} + {i + 1} = <<{i}+{i + 1}={2 * i + 1}>>{2 * i + 1} #### {2 * i + 1}"}
           for i in range(1, 4)]
    buf = io.BytesIO()
    pq.write_table(pa.Table.from_pylist(gsm), buf)
    hover = [{"uid": f"u{i}", "claim": f"The claim number {i} is about a river and a city and a bridge", "label": "SUPPORTED",
              "num_hops": 2, "hpqa_id": f"h{i % 2}", "supporting_facts": [["Title", 0]]} for i in range(5)]
    csv_ = "text,sarcastic\nwhat a lovely day to be stuck in traffic again,1\nthis is just fine,0\n"
    csvc = "text_0,text_1,sarcastic_id\nso happy to wait forever here,fine with waiting here,0\n"

    def fake(url, timeout=300):
        if url.endswith(".parquet"):
            return buf.getvalue()
        if url.endswith(".json"):
            return json.dumps(hover).encode()
        return (csvc if "_C_" in url else csv_).encode()
    monkeypatch.setattr(R, "fetch", fake)
    out = R.cmd_fetch_src(type("A", (), {"root": str(root)})())
    assert out["sources"]["gsm8k"]["rows"] == 3 and out["sources"]["hover"]["rows"] == 5 and out["sources"]["isarcasmeval"]["rows"] == 8   # A_En 2, A_Ar 2, B_En 2, C_En 1, C_Ar 1
    assert out["sources"]["gsm8k"]["as_expected"] is False and out["sources"]["hover"]["as_expected"] is False          # 1,319 / 4,000 expected
    ids = json.loads((di / "record_ids.json").read_text())
    assert D.sha_hex(D.norm(gsm[0]["question"])) in ids["gsm8k_question_sha256"] and ids["hover_uid"] == sorted(f"u{i}" for i in range(5))
    assert ids["hover_group"] == ["h0", "h1"] and D.sha_hex(D.norm("what a lovely day to be stuck in traffic again")) in ids["isarcasm_text_sha256"]
    assert set(out["files"]) == set(D.SRC_FILES) and out["files"][D.SRC_FILES[0]]["rows"] == 3
    rows = [json.loads(x) for x in (root / D.SRC_FILES[2]).read_text().splitlines()]
    assert {r["track"] for r in rows} == {"task_A_En", "task_A_Ar", "task_B_En", "task_C_En", "task_C_Ar"}
    unc = build_di03(root)
    (di / "kit_pin.json").write_text(json.dumps(kit_pin(unc)))
    pins = R.cmd_finalize(type("A", (), {"root": str(root)})())
    assert pins["di_src_splits"]["complete"] is False and any("gsm8k: 3 rows, expected 1319" in x for x in pins["di_src_splits"]["gaps"])
    assert "tracks" in pins["di_src_splits"]["sources"]["isarcasmeval"] and "revision" in pins["di_src_splits"]["sources"]["hover"]


def test_the_pins_of_the_real_g13_di_folder_hold_the_ruling_numbers():
    """The real pin files written by di_register.py pin / fetch-src (counts and hashes only)."""
    kit = json.loads((C2B / "g13_di" / "kit_pin.json").read_text())
    assert kit["edition"] == "release-v3" and kit["repo"].endswith("apolinario/decision-index") and len(kit["commit"]) == 40
    assert kit["files"][R.MANIFEST_PATH]["sha256"] == R.EXPECTED_SHA[R.MANIFEST_PATH] and kit["files"][R.SUITE_MD]["sha256"] == R.EXPECTED_SHA[R.SUITE_MD]
    assert all(all(v.values()) for v in kit["same_at"].values())                       # the same two files at the 0.3 edition commits
    assert len(kit["benchmarks"]) == 37 and len(kit["added"]) == 7 and kit["requests"] == 110201
    src = json.loads((C2B / "g13_di" / "src_pins.json").read_text())
    assert src["sources"]["gsm8k"]["rows"] == 1319 and src["sources"]["hover"]["rows"] == 4000 and src["sources"]["isarcasmeval"]["rows"] == 4600
    assert src["sources"]["gsm8k"]["revision"].startswith("740312a") and src["sources"]["hover"]["revision"].startswith("39b8469")
    assert src["sources"]["isarcasmeval"]["revision"].startswith("dfc708b")
