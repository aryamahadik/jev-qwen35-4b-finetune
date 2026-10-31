import ast
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from oc1 import common as C
from oc1 import export_driver as ED

ROOT = Path(__file__).resolve().parents[1]
ORIG = C.LEAN / "hosting" / "export_c1_merged.py"
GEN = ROOT / "oc1" / "export_pure.py"
sys.path.insert(0, str(ROOT))
import tools_gen_export_pure as G  # noqa: E402


def segs(path, names):
    text = Path(path).read_text()
    out = {}
    for n in ast.parse(text).body:
        nm = None
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            nm = n.name
        elif isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            nm = n.targets[0].id
        if nm in names:
            out[nm] = ast.get_source_segment(text, n)
    return out


def test_generated_file_is_current_and_verbatim():
    assert G.main(["--check"]) == 0, "oc1/export_pure.py is stale: run tools_gen_export_pure.py"
    names = set(G.DEFS) | set(G.ASSIGNS)
    a, b = segs(ORIG, names), segs(GEN, names)
    assert set(a) == set(b) == names
    for n in names:
        assert a[n] == b[n], f"{n} differs from hosting/export_c1_merged.py"


def test_pins_and_constants_agree_with_the_sglang_host():
    sys.path.insert(0, str(C.LEAN / "hosting"))
    import sglang_host as SH
    from oc1 import export_pure as E
    assert E.C1_ADAPTER_SHA256 == C.C1_ADAPTER_SHA256 == SH.C1_ADAPTER_SHA256
    assert E.MERGED_NAME == C.MERGED_NAME == SH.MERGED_NAME and E.BASE == C.BASE and E.REVISION == C.REVISION
    assert E.EXPECT_LAYOUT == ("schema_branch_mark", "cygnet")


def test_hf_cache_mirror_and_reference_comparison(tmp_path):
    old = tmp_path / "old"
    snap = old / "hf" / "hub" / "models--Qwen--Qwen3.5-4B" / "snapshots" / "abc"
    snap.mkdir(parents=True)
    (snap / "config.json").write_text("{}")
    (snap / "model.safetensors-00001-of-00002.safetensors").write_bytes(b"x" * 10)
    mirror = ED.build_hf_cache(old, tmp_path / "hf", "Qwen/Qwen3.5-4B", "abc")
    assert (tmp_path / "hf" / "hub" / "models--Qwen--Qwen3.5-4B" / "refs" / "main").read_text() == "abc"
    assert sorted(p.name for p in mirror.iterdir()) == ["config.json", "model.safetensors-00001-of-00002.safetensors"]
    assert all(p.is_symlink() for p in mirror.iterdir()) and (mirror / "config.json").read_text() == "{}"
    out = tmp_path / "out"
    out.mkdir()
    (out / "merge_manifest.json").write_text(json.dumps({"files": {"a": {"sha256": "1"}, "b": {"sha256": "2"}}}))
    same = ED.compare_with_reference(out, {"files": {"a": {"sha256": "1"}, "b": {"sha256": "2"}}})
    assert same["identical"] and same["differing"] == []
    diff = ED.compare_with_reference(out, {"files": {"a": {"sha256": "1"}, "b": {"sha256": "9"}, "c": {"sha256": "3"}}})
    assert not diff["identical"] and diff["differing"] == ["b", "c"]
    assert ED.compare_with_reference(out, None) == {"reference": None}


def test_the_merged_checkpoint_manifest_shipped_for_the_comparison_is_c1s():
    man = json.loads((ROOT / "data" / "ref_speed2_merge_manifest.json").read_text())
    assert man["adapter_sha256"] == C.C1_ADAPTER_SHA256 and man["layout"] == "base" and len(man["files"]) == 17
    assert man["checks"]["passed"] is True
