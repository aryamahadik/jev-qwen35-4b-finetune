"""The template / wording-pool hash export (G-W3 template-hash currency): hashes only, deterministic, complete, and current."""
import json
import os

import gen_hash_export as HX
import pool_loader as PL


def test_export_is_hashes_only_and_complete():
    exp = HX.build_export(created="2026-10-18T00:00:00Z")
    text = json.dumps(exp)
    ent = PL.load_entries()
    n = 0
    for k, lst in ent.items():
        assert exp["wording_pool"]["keys"][k]["count"] == len(lst)
        assert len(exp["wording_pool"]["keys"][k]["template_sha256"]) == len(lst)
        for t in lst:
            n += 1
            assert len(t) < 12 or t not in text            # no wording text in the export
    assert exp["wording_pool"]["n_templates"] == n
    assert set(exp["wording_pool"]["files"]) == {"fragments.json", "q_arith.json", "q_logic.json", "q_causal.json", "q_temporal.json", "q_table.json",
                                                 "predicate_vocab.json", "hx_forms.json"}
    for d, hs in exp["predicate_vocab"].items():
        assert len(hs) == 8 and all(len(h) == 64 for h in hs)
    for ph in (p for v in PL.predicate_vocab().values() for p in v):
        assert ph not in text
    assert exp["question_templates_solver_b"]["real"]["n_templates"] == 1176
    assert "NAMES_MANIFEST_V1.json" in exp["names"] and "namespace.py" in exp["names"]
    assert exp["unbuilt_wording"]["note"]["forms"][0] == "HX-E"


def test_export_is_deterministic_and_a_change_moves_the_template_hash():
    a = HX.build_export(created="x")
    b = HX.build_export(created="y")
    assert a["template_hash"] == b["template_hash"] and a["export_sha256"] == b["export_sha256"]
    ent = PL.load_entries()
    k = "q.AR-F1"
    before = HX.template_block({k: ent[k]})
    changed = list(ent[k])
    changed[0] = changed[0] + " "
    after = HX.template_block({k: changed})
    assert before[k]["key_sha256"] != after[k]["key_sha256"] and before[k]["template_sha256"][0] != after[k]["template_sha256"][0]
    assert before[k]["template_sha256"][1:] == after[k]["template_sha256"][1:]


def test_export_on_disk_is_current():
    """G-W3: the HASH_EXPORT.json next to the code matches the files as they are. Re-run `python3 gen_hash_export.py --write` after ANY template, table,
    pool or code change (and re-make the rows of the changed templates)."""
    assert os.path.isfile(HX.OUT), "run python3 gen_hash_export.py --write"
    disk = json.load(open(HX.OUT))
    disk.pop("created_utc", None)
    live = HX.build_export()
    live.pop("created_utc", None)
    assert disk == live
