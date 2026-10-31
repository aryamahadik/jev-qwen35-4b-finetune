"""write_checks.py: the SPEC 8 outputs (yn2b_checks.json, yn2b_summary.json) on a fixture tree."""
from __future__ import annotations

import json

import write_checks as wc
import yn2b_common as yc
from conftest import write_jsonl


def _rows(src="gd_gen3_toy", n=40, card_bias=False):
    out = []
    for i in range(n):
        g = i % 2
        card = "- Yes: a\n- No: b" if (card_bias and g) else "- yes: a\n- no: b"
        out.append({"id": f"r{i}", "source": src, "state": "s" * (50 + i % 7), "qtype": "noul", "gold": g,
                    "options": None, "card": card, "role": "aff",
                    "meta": {"latent_id": f"L{i // 2}", "fmt": ["json", "kv"][i // 2 % 2], "tier": "easy",
                             "polarity": 0, "view": "base", "qkind": "yn"}})
    out.append({"id": "c1", "source": src, "state": "x", "qtype": "choice", "gold": "a", "options": ["a", "b"],
                "card": None, "role": "choice", "meta": {"latent_id": "L99", "qkind": "jb", "view": "jb_letter"}})
    return out


def test_artefact_probe_flags_a_card_style_leak():
    ok = wc.artefact_probe(_rows())
    assert ok["under_0.05"] and ok["rows"] == 40 and ok["yes_share"] == 0.5
    bad = wc.artefact_probe(_rows(card_bias=True))
    assert bad["card_style_upper"] == 1.0 and not bad["under_0.05"]


def test_counts_and_inputs_match():
    rows = _rows()
    c = wc.counts(rows, [{"type": "complement", "a": "r0", "b": "r1"}])["gd_gen3_toy"]
    assert (c["rows"], c["yes_no"], c["jb_letter"], c["choice"], c["latents"]) == (41, 40, 1, 0, 21)
    assert c["relations"] == {"complement": 1}
    assert wc.report_inputs_match({"train": {"sha256": "a"}, "dev": {"sha256": "b"}}, {"train": "a", "dev": "c"}) == \
        {"train": True, "dev": False}


def test_main_writes_both_files_and_flags_stale_reports(tmp_path, monkeypatch):
    y = tmp_path / "yn2b"
    raw = tmp_path / "raw"
    write_jsonl(raw / "gen3_toy.jsonl", [{"rid": "x"}])
    write_jsonl(raw / "dev" / "gen3_toy.jsonl", [{"rid": "y"}])
    sha_t, sha_d = yc.sha256_file(raw / "gen3_toy.jsonl"), yc.sha256_file(raw / "dev" / "gen3_toy.jsonl")
    y.mkdir()
    (y / "agree.json").write_text(json.dumps({"inputs": {"train": {"sha256": sha_t}, "dev": {"sha256": "old"}},
                                              "parts": {"train": {"rows": 1, "agree": 1}, "dev": {"rows": 1, "agree": 1}}}))
    (y / "gate.json").write_text(json.dumps({"inputs": {"train": {"sha256": sha_t}, "dev": {"sha256": sha_d}},
                                             "verdict": {"green": True}, "mv_core_checks": {"train": {"balance": True}}}))
    (y / "blind.json").write_text(json.dumps({"final": {"n": 100, "agree": 99, "open_generator_bugs": 0}}))
    monkeypatch.setattr(yc, "YN2B", y)
    monkeypatch.setattr(wc, "FAMILIES", {"gen3_toy": ("F9", "agree.json", "gate.json", "blind.json")})
    write_jsonl(tmp_path / "t.jsonl", _rows())
    write_jsonl(tmp_path / "di.jsonl", _rows())
    (tmp_path / "dec.json").write_text(json.dumps({"7.1_ohs3_hit_units_per_family": {}, "template_failures": []}))
    (tmp_path / "uns.json").write_text(json.dumps({"problems": []}))
    checks, summary = wc.main(["--assembled", f"train={tmp_path / 't.jsonl'},dev_iid={tmp_path / 'di.jsonl'}",
                               "--raw-dir", str(raw), "--decontam", str(tmp_path / "dec.json"),
                               "--unseen", str(tmp_path / "uns.json"), "--no-mv-checks", "--out-checks", str(tmp_path / "c.json"),
                               "--out-summary", str(tmp_path / "s.json")])
    f = checks["families"]["gd_gen3_toy"]
    assert f["decide2"]["report_matches_current_build"] == {"train": True, "dev": False}
    assert f["gate"]["inputs_match_current_build"] == {"train": True, "dev": True} and f["gate"]["green"]
    assert f["blind"]["rounds"][-1] == {"build": "final", "n": 100, "agree": 99, "open_generator_bugs": 0}
    assert checks["problems"] == ["F9: decide2 report is not on the current build"] and not checks["all_checks_pass"]
    assert summary["totals"]["train"]["rows"] == 41 and json.loads((tmp_path / "s.json").read_text())["sha256"]


def test_mv_checks_as_assembled_on_toy_family(tmp_path):
    """mv_core.run_checks on raw rows with a view left out (the toy family is balanced with all its views)."""
    import mv_core as mv
    import toy_family as toy
    fb = mv.FamilyBuilder(toy.KEY, generator_file=toy.__file__, raw_dir=tmp_path / "raw", defs_dir=tmp_path / "defs",
                          manifest=tmp_path / "m.jsonl", tier_shares={"easy": 0.3, "standard": 0.4, "hard": 0.3})
    toy.build(fb, "train", 200)
    fb.write()
    full = wc.mv_checks(toy.KEY, tmp_path / "raw")
    assert full["train"]["rows"] > 0 and full["train"]["views_left_out"] == 0
    rows, _ = mv.read_raw(toy.KEY, "train", tmp_path / "raw")
    v = sorted({r["meta"].get("view") for r in rows} - {"base"})[0]
    part = wc.mv_checks(toy.KEY, tmp_path / "raw", frozenset({(toy.KEY, v)}))
    assert part["train"]["views_left_out"] == sum(r["meta"].get("view") == v for r in rows)
    assert part["train"]["rows"] == full["train"]["rows"] - part["train"]["views_left_out"]
