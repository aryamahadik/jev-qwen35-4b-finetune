"""gather_names.py: the SPEC 7.7 name list for check_yn2b --names (pool persons / organisations shown in rows)."""
from __future__ import annotations

import json

import gather_names as gn
from conftest import write_jsonl


def _pool_bits():
    import mv_core as mv
    P = mv._pools()
    return P["train"]["first"][5], P["dev_iid"]["last"][7], P["devx"]["stem"][3], mv._ORG_SUFFIX


def test_persons_and_orgs_from_any_split_pool():
    f, l, st, suf = _pool_bits()
    idx = gn.pool_index()
    txt = f"Filed by {f} {l} for {st} {suf[0]}; reviewed by Alice Smith of Acme {suf[0]}. {st} alone is no name."
    got = gn.names_in_text(txt, idx)
    assert got == {f"{f} {l}", f"{st} {suf[0]}"}
    multi = [s for s in suf if " " in s][0]  # a two-word suffix ("Credit Union")
    assert gn.names_in_text(f"{st} {multi} paid", idx) == {f"{st} {multi}"}


def test_gather_cli_merges_family_files_and_rows(tmp_path):
    f, l, st, suf = _pool_bits()
    rows = [{"source": "gd_gen3_x", "state": f"{f} {l} wrote", "instructions": "q?", "options": None, "card": None},
            {"source": "gd_gen3_y", "state": "none", "instructions": "q?", "options": [f"{st} {suf[1]}"], "card": None}]
    write_jsonl(tmp_path / "t.jsonl", rows)
    (tmp_path / "names_gen3_z.json").write_text(json.dumps({"gd_gen3_z": ["Zed Name"]}))
    res = gn.main(["--train", str(tmp_path / "t.jsonl"), "--family-dir", str(tmp_path), "--out", str(tmp_path / "n.json")])
    assert res == {"gd_gen3_x": [f"{f} {l}"], "gd_gen3_y": [f"{st} {suf[1]}"], "gd_gen3_z": ["Zed Name"]}
    assert json.loads((tmp_path / "n.json").read_text()) == res


def test_family_files_reads_names_json(tmp_path):
    (tmp_path / "names_gen3_a.json").write_text(json.dumps({"gd_gen3_a": ["A B", " ", "C D"]}))
    (tmp_path / "other.json").write_text(json.dumps({"gd_gen3_b": ["X"]}))
    assert dict(gn.family_files(tmp_path)) == {"gd_gen3_a": {"A B", "C D"}}


def test_one_word_names_only_when_shown_alone(tmp_path):
    rows = [{"source": "gd_gen3_x", "state": "Heron Energy filed. Later Heron Energy paid. Vexa signed the form.",
             "instructions": "Did Gaman Goundov pay?", "options": None, "card": None}]
    fam = {"gd_gen3_x": {"Heron", "Heron Energy", "Vexa", "Gaman", "Gaman Goundov", "Unused"}}
    rows[0]["state"] += " Bus to Gaman Primary daily."
    res = gn.gather(rows, [fam])
    assert set(res["gd_gen3_x"]) >= {"Heron Energy", "Vexa", "Gaman Goundov", "Gaman Primary"}
    assert not {"Heron", "Gaman", "Unused"} & set(res["gd_gen3_x"])
    rows[0]["state"] += " Heron alone. Herons fly."
    assert "Heron" in gn.gather(rows, [fam])["gd_gen3_x"]
    assert gn.single_name_forms({"f": [{"state": "Paid Heron. Heron, then Energy.", "instructions": "", "options": None,
                                         "card": None}]}, {"f": {"Heron"}}) == {"f": {"Paid Heron", "Heron"}}
