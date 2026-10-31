"""Tests for c2_build/meta_src/build_never_train.py (A75 a). CPU only; the manifest is built into tmp_path (the real one is only
compared when it exists). Run from lean/:
  ../.venv/bin/python -B -m pytest -q c2_build/tests/test_build_never_train.py
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
sys.path.insert(0, str(C2B / "meta_src"))
import build_never_train as bnt  # noqa: E402
import mix_c2 as m  # noqa: E402

LINES = bnt.PREREG.read_text(encoding="utf-8").splitlines()
ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.\-]*/[A-Za-z0-9][A-Za-z0-9_.\-]*")

# the 13 A42-D 13.3 entries, as PREREG words them (independent of the tool's table)
D133_TEXT = ["BFCL V4 selection + irrelevance", "InjecAgent", "NotInject", "R-Judge", "CRUXEval-O as MCQ", "EquiBench Python",
             "When2Call test", "AgentProcessBench", "ATBench-Codex", "ACPBench", "CodeJudgeBench",
             "LiveCodeBench post-cutoff execution", "SWE-bench Verified"]


def block(start_pat: str, end_pat: str) -> tuple[int, list[str]]:
    i = next(k for k, x in enumerate(LINES) if start_pat in x)
    j = next(k for k in range(i + 1, len(LINES)) if end_pat in LINES[k])
    return i + 1, LINES[i:j]


def a40_ids() -> list[str]:
    _, blk = block("**(a) Never-train additions.**", "C1 already trained on clinc150")
    txt = " ".join(re.sub(r"^\s*>\s?", "", x) for x in blk)
    txt = txt.split("benchmark is added to the C2 never-train list", 1)[1]
    return [x.rstrip(".,;") for x in ID_RE.findall(txt)]


@pytest.fixture(scope="module")
def doc():
    return bnt.build()


@pytest.fixture(scope="module")
def manifest(doc, tmp_path_factory):
    p = tmp_path_factory.mktemp("nt") / "c2_never_train_manifest.json"
    assert bnt.main(["--out", str(p)]) == 0
    return p


def test_every_prereg_a40_name_is_present(doc):
    ids = a40_ids()
    assert len(ids) == 22                                              # 20 hugging face ids + angular/angular + vitejs/vite (+ the 2 on line 2139's list)
    names = set(doc["names"])
    for i in ids:
        assert i.lower() in names, i
    got = {e["prereg_text"].lower() for e in doc["entries"] if e["list"] == bnt.A40}
    assert got == {i.lower() for i in ids}                             # no unlisted A40 entry, none missing


def test_every_prereg_d133_name_is_present(doc):
    n0, blk = block("**13.3 Public anchors**", "**13.4 General accuracy:**")
    txt = re.sub(r"\s+", " ", " ".join(re.sub(r"^\s*>\s?", "", x) for x in blk))
    for t in D133_TEXT:
        assert t in txt, t
    got = [e["prereg_text"] for e in doc["entries"] if e["list"] == bnt.D133]
    assert got == D133_TEXT
    for e in doc["entries"]:
        if e["list"] == bnt.D133:
            assert e["prereg_text"].lower() in doc["names"]
    # the stated line numbers are the real ones
    for e in doc["entries"]:
        a, b = e["prereg_lines"]
        blob = re.sub(r"\s+", " ", " ".join(re.sub(r"^\s*>\s?", "", x) for x in LINES[a - 1:b]))
        assert e["prereg_text"] in blob
    assert doc["counts"]["entries"] == 35 and doc["counts"]["a40a"] == 22 and doc["counts"]["d133"] == 13


def test_ids_named_by_name_cover_the_task_shorthand(doc):
    names = set(doc["names"])
    for n in ["prompt-injections", "jailbreak-classification", "spml", "jailbreaksovertime", "openai-moderation", "aegis-2.0", "aegis 2.0",
              "gretel-pii", "privy", "nemotron-pii", "halueval", "clinc_oos", "clinc150", "massive", "snips", "banking77", "bfcl",
              "consumer-finance-complaints", "angular/angular", "vitejs/vite", "esci", "typed-decisions", "jevforge-mind2web", "jev-bench",
              "bfcl v4", "injecagent", "notinject", "r-judge", "cruxeval", "equibench", "when2call", "agentprocessbench", "atbench",
              "acpbench", "codejudgebench", "livecodebench", "swe-bench"]:
        assert n in names, n


def test_no_unlisted_name_added(doc, monkeypatch):
    # every name carries its entry's core token and every alias the deny-list contributes is really in the deny-list
    by_id = {e["id"]: e for e in bnt.E}
    for e in doc["entries"]:
        for n in e["names"]:
            assert any(c in bnt.norm(n) for c in by_id[e["id"]]["cores"]), (e["id"], n)
    assert set(doc["names"]) == {n for e in doc["entries"] for n in e["names"]}
    assert all(n == n.lower() for n in doc["names"])
    # an unrelated name smuggled into an entry, a made-up entry or a made-up deny-list alias is refused
    bad = dict(by_id["A40a-08"], extra=("squad2",))
    monkeypatch.setattr(bnt, "E", [bad if x["id"] == "A40a-08" else x for x in bnt.E])
    with pytest.raises(SystemExit, match="core token"):
        bnt.build()
    monkeypatch.undo()
    fake = dict(by_id["A40a-08"], id="A40a-99", text="someorg/squad2", hf="someorg/squad2", cores=("squad2",))
    monkeypatch.setattr(bnt, "E", bnt.E + [fake])
    with pytest.raises(SystemExit, match="not on PREREG_FINAL.md"):
        bnt.build()
    monkeypatch.undo()
    bad = dict(by_id["A40a-08"], dl=("totally made up",))
    monkeypatch.setattr(bnt, "E", [bad if x["id"] == "A40a-08" else x for x in bnt.E])
    with pytest.raises(SystemExit, match="deny-list alias"):
        bnt.build()


def test_a_wrong_line_number_is_refused(monkeypatch):
    bad = dict(bnt.E[0], lines=(2000, 2000))
    monkeypatch.setattr(bnt, "E", [bad] + bnt.E[1:])
    with pytest.raises(SystemExit, match="is not on PREREG_FINAL.md line"):
        bnt.build()


def test_format_loads_with_mix_c2(manifest, doc):
    never = m.load_never_train(manifest, None)
    assert never["names"] == set(doc["names"]) | {a["name"].lower() for a in doc["anchors"]}
    assert never["paths"] == {a["path"] for a in doc["anchors"]}
    assert never["sha256"] == {a["sha256"] for a in doc["anchors"]}
    assert set(json.loads(manifest.read_text())) >= {"names", "anchors"}
    merged = m.merge_di_never_train(never)                              # the DI file merges on top, nothing is lost
    assert merged["names"] >= never["names"] and merged["sha256"] >= never["sha256"] and merged["paths"] >= never["paths"]
    assert len(merged["names"]) == len(never["names"]) + len(merged["names"] - never["names"])


def test_anchor_files_are_outside_never_open_paths_and_hashed(doc):
    for a in doc["anchors"]:
        p = Path(a["path"])
        assert p.is_file() and bnt.never_open(p) is None
        assert a["sha256"] == bnt.sha256_file(p) and re.fullmatch(r"[0-9a-f]{64}", a["sha256"])
        assert "external_quarantine" not in a["path"] and "ohs" not in a["path"].lower() and "sealed" not in a["path"].lower()
    assert [a["entry"] for a in doc["anchors"]] == ["D133-05"]


def test_a_never_open_anchor_candidate_is_refused(monkeypatch):
    monkeypatch.setattr(bnt, "ANCHOR_CANDIDATES", {"D133-05": [("cruxeval", "ohs4_sealed/x.jsonl", "n")]})
    with pytest.raises(SystemExit, match="never-open"):
        bnt.build()
    monkeypatch.setattr(bnt, "ANCHOR_CANDIDATES", {"D133-05": [("cruxeval", "../bench/external_quarantine/x.jsonl", "n")]})
    with pytest.raises(SystemExit, match="never-open"):
        bnt.build()


def test_anchor_row_problems_refuses_an_anchor_row(manifest):
    names = m.load_never_train(manifest, None)["names"]
    for src in ["banking77", "clinc_oos:train", "bfcl_v4_selection", "cruxeval-o", "when2call", "halueval_qa", "deepset/prompt-injections",
                "Aegis 2.0", "tasksource/esci:x"]:
        assert m.anchor_row_problems([{"source": src}], names), src
    assert m.anchor_row_problems([{"source": "x", "meta": {"text_source": {"dataset": "HaluEval"}}}], names)
    rep = m.anchor_row_problems([{"source": "snips"}, {"source": "t01_ncd"}, {"source": "pubmedqa"}], names)
    assert len(rep) == 1 and "snips" in rep[0] and "t01_ncd" not in rep[0] and "pubmedqa" not in rep[0]
    assert m.anchor_row_problems([{"source": "t01_ncd"}, {"source": "gb_card", "meta": {"text_source": {"dataset": "wiki_x"}}}], names) == []


def test_anchor_row_problems_plain_string_text_source(manifest):
    names = m.load_never_train(manifest, None)["names"]
    assert m.anchor_row_problems([{"source": "x", "meta": {"text_source": "injecagent"}}], names)
    assert m.anchor_row_problems([{"source": "x", "meta": {"text_source": "HaluEval"}}], names)
    assert m.anchor_row_problems([{"source": "x", "meta": {"text_source": {"dataset": "injecagent"}}}], names)
    assert m.anchor_row_problems([{"source": "x", "meta": {"text_source": "c2_gblock"}}, {"source": "y", "meta": {"text_source": None}},
                                  {"source": "z", "meta": {"text_source": "api.ror.org"}}], names) == []


def test_anchor_file_and_its_sha_are_refused_as_training_inputs(manifest, doc):
    never = m.load_never_train(manifest, None)
    a = doc["anchors"][0]
    assert m.train_path_problem(a["path"], never["paths"])
    assert m.train_path_problem("some/other/copy.jsonl", (), never["sha256"], a["sha256"])
    assert m.train_path_problem("some/other/copy.jsonl", never["paths"], never["sha256"], "0" * 64) is None


def test_output_is_deterministic_and_matches_the_written_manifest(manifest, tmp_path):
    p2 = tmp_path / "again.json"
    assert bnt.main(["--out", str(p2)]) == 0
    assert p2.read_bytes() == manifest.read_bytes()
    assert bnt.main(["--out", str(manifest)]) == 0                       # same bytes: no --force needed
    manifest.write_text("{}")
    assert bnt.main(["--out", str(manifest)]) == 2                       # a different existing file is not overwritten
    assert manifest.read_text() == "{}"
    assert bnt.main(["--out", str(manifest), "--force"]) == 0
    assert manifest.read_bytes() == p2.read_bytes()
    if bnt.OUT.is_file():
        assert bnt.OUT.read_bytes() == p2.read_bytes()                   # the real manifest is what the tool builds now


def test_dry_writes_nothing(tmp_path):
    p = tmp_path / "x.json"
    assert bnt.main(["--dry", "--out", str(p)]) == 0 and not p.exists()
