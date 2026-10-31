"""VOICE hash export: hashes only, deterministic, covers every template, and is current (template-hash currency)."""
import json
import os

import voice_hash_export as HX


def test_export_is_hashes_only_and_complete():
    exp = HX.build_export(created="2026-10-18T00:00:00Z")
    text = json.dumps(exp)
    with open(os.path.join(HX.HERE, "pools", "natural_phrase_table.json")) as f:
        nat = json.load(f)
    n = 0
    for op, lst in nat["ops"].items():
        assert exp["pools"]["natural_phrase_table"]["ops"][op]["count"] == len(lst)
        for t in lst:
            n += 1
            assert t not in text
    assert n == 152
    for w in list(nat["flag_phrases"].values()) + nat["folder_words"]:
        assert '"%s"' % w not in text
    assert "vcommon.table_hashes.symbol_table" in exp["tables"]
    assert exp["unbuilt"]["generators"][0].startswith("VGEN-C")


def test_export_is_deterministic():
    a, b = HX.build_export(created="x"), HX.build_export(created="y")
    assert a["template_hash"] == b["template_hash"] and a["export_sha256"] == b["export_sha256"]


def test_export_on_disk_is_current():
    assert os.path.isfile(HX.OUT), "run python3 voice_hash_export.py --write"
    disk = json.load(open(HX.OUT))
    disk.pop("created_utc", None)
    live = HX.build_export()
    live.pop("created_utc", None)
    assert disk == live
