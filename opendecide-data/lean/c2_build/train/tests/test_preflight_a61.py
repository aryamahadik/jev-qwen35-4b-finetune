"""Tests for the A61 additions of preflight_c2.py (PREREG Ruling A61 e / f; program fixes 5 and 6): the a61_85 check (the 8.5 gate before
training), the c2_tmax.json guard, the credit coverage FAIL. Fixture folders under tmp only: no real input, result or exit file is read, no sealed
or ohs path is named, source_name_check.py is never run.
  cd lean/c2_build/train && ../../../.venv/bin/python -B -m pytest -q tests/test_preflight_a61.py"""
import hashlib
import json
import sys
from pathlib import Path

import pytest

TRAIN = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TRAIN))
import c2_check as cc  # noqa: E402
import preflight_c2 as pf  # noqa: E402

IN, RES, EX = pf.A61_FILES


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def row(i, source):
    return json.dumps({"id": f"r{i}", "source": source, "text": "a c2_md_zzz mention in the text must not count"})


def make(tmp, mix_sources=("c2_md_a", "c2_md_b", "c2_sb5", "gd_x"), input_ids=("md_a", "md_a#2", "md_b", "md_c", "SB5_uci293", "SB5_uci293#doi"),
         lines=("md_a PASS", "md_b PASS", "md_c PASS", "SB5_uci293 PASS"), exit_txt="0\n", record=True, log_after=None):
    """A mix on disk, the three final-run files and A61_EDIT_RECORD.json (shas logged, in a nested layout)."""
    d = tmp / "di_train"
    d.mkdir()
    mix = tmp / "c2_train.jsonl"
    mix.write_text("\n".join(row(i, s) for i, s in enumerate(mix_sources)) + "\n")
    (d / IN).write_text(json.dumps({"sources": [{"id": i, "name": "n"} for i in input_ids]}))
    (d / RES).write_text("".join(x + "\n" for x in lines))
    (d / EX).write_text(exit_txt)
    if record:
        rec = {"step": 9, "before": {n: sha((d / n).read_bytes()) for n in (IN,)},
               "after": {"files": [{"file": f"zed_orch/di_train/{n}", "sha256": sha((d / n).read_bytes())} for n in (RES, EX)],
                         IN: {"sha256": sha((d / IN).read_bytes())}}}
        (d / pf.A61_RECORD).write_text(json.dumps(rec))
    return mix, d


def problems(tmp_path, **kw):
    mix, d = make(tmp_path, **{k: v for k, v in kw.items() if k not in ("tamper", "drop")})
    for n, fn in (kw.get("tamper") or {}).items():
        fn(d / n)
    for n in kw.get("drop") or ():
        (d / n).unlink()
    return pf.check_a61_85(mix, d)


def test_passes_when_every_gated_source_in_the_mix_has_one_pass_line(tmp_path):
    p, info = problems(tmp_path)
    assert p == [] and info["gated_in_mix"] == ["SB5_uci293", "md_a", "md_b"] and info["pass"] == 4 and info["hit"] == 0


def test_a_text_mention_of_a_prefix_is_not_a_gated_row(tmp_path):
    mix, d = make(tmp_path, mix_sources=("gd_x", "c2_md_", "c2_sb5_other", "T28"))
    assert pf.gated_ids_in_mix(mix) == set()
    assert pf.check_a61_85(mix, d)[0] == []


def test_no_gated_row_passes_and_says_so_even_without_any_8_5_file(tmp_path):
    mix = tmp_path / "c2_train.jsonl"
    mix.write_text(row(1, "gd_x") + "\n" + row(2, "T28") + "\n")
    p, info = pf.check_a61_85(mix, tmp_path / "does_not_exist")
    assert p == [] and "nothing to check" in info["note"] and info["gated_in_mix"] == []


@pytest.mark.parametrize("name", [IN, RES, EX, pf.A61_RECORD])
def test_a_missing_file_fails(tmp_path, name):
    p, _ = problems(tmp_path, drop=[name])
    assert p and any("missing" in x or "not readable" in x for x in p)


def test_a_missing_mix_file_fails(tmp_path):
    mix, d = make(tmp_path)
    mix.unlink()
    p, _ = pf.check_a61_85(mix, d)
    assert p and "not readable" in p[0]


@pytest.mark.parametrize("name", [IN, RES, EX])
def test_a_sha_mismatch_fails(tmp_path, name):
    p, _ = problems(tmp_path, tamper={name: lambda f: f.write_bytes(f.read_bytes() + b" ")})
    assert len(p) == 1 and "differs from the logged" in p[0] and name in p[0]


@pytest.mark.parametrize("name", [IN, RES, EX])
def test_a_file_with_no_logged_sha_fails(tmp_path, name):
    mix, d = make(tmp_path)
    rec = json.loads((d / pf.A61_RECORD).read_text())
    text = json.dumps(rec).replace(name, "other_name.txt")
    (d / pf.A61_RECORD).write_text(text)
    p, _ = pf.check_a61_85(mix, d)
    assert any(f"logs no sha256 for {name}" in x for x in p)


def test_two_different_logged_shas_for_one_file_fail(tmp_path):
    mix, d = make(tmp_path)
    rec = json.loads((d / pf.A61_RECORD).read_text())
    rec["again"] = {IN: "0" * 64}
    (d / pf.A61_RECORD).write_text(json.dumps(rec))
    assert any("differs from the logged" in x for x in pf.check_a61_85(mix, d)[0])


def sub(tmp, name):
    q = tmp / name
    q.mkdir()
    return q


def relog(d):
    """Re-log the current shas (a tampered file with a matching record: the content rules still apply)."""
    rec = {"final_85": {n: sha((d / n).read_bytes()) for n in pf.A61_FILES}}
    (d / pf.A61_RECORD).write_text(json.dumps(rec))


def check(tmp_path, **kw):
    mix, d = make(tmp_path, **kw)
    relog(d)
    return pf.check_a61_85(mix, d)[0]


@pytest.mark.parametrize("code", ["2\n", "1\n", "", "\n", "00\n", "0 \n0\n", "x\n"])
def test_an_exit_other_than_0_fails(tmp_path, code):
    p = check(tmp_path, exit_txt=code)
    if code.strip() == "0":
        assert p == []
    else:
        assert p and "exit file holds" in p[0]


def test_exit_0_with_or_without_a_newline_passes(tmp_path):
    assert check(tmp_path, exit_txt="0") == []


@pytest.mark.parametrize("bad", ["md_a PASS-NONBINDING", "md_a MAYBE", "md_a  PASS", "md_a", "PASS md_a", "md_a PASS extra", " md_a PASS", "md_a pass", "", "Traceback ..."])
def test_a_bad_line_fails(tmp_path, bad):
    lines = ("md_a PASS", bad, "md_b PASS", "md_c PASS", "SB5_uci293 PASS")
    p = check(tmp_path, lines=lines)
    assert any("not '<id> PASS' or '<id> HIT'" in x for x in p), (bad, p)


def test_a_missing_id_fails(tmp_path):
    p = check(tmp_path, lines=("md_a PASS", "md_b PASS", "SB5_uci293 PASS"))                         # md_c has no line
    assert any("no result line" in x and "md_c" in x for x in p)
    assert any("no result line" in x for x in check(sub(tmp_path, "empty"), lines=()))


def test_a_duplicate_id_fails(tmp_path):
    p = check(tmp_path, lines=("md_a PASS", "md_b PASS", "md_b PASS", "md_c PASS", "SB5_uci293 PASS"))
    assert any("more than one result line" in x and "md_b" in x for x in p)
    p = check(sub(tmp_path, "x"), lines=("md_a PASS", "md_b PASS", "md_b HIT", "md_c PASS", "SB5_uci293 PASS"))
    assert any("more than one result line" in x for x in p)


def test_an_extra_id_fails(tmp_path):
    p = check(tmp_path, lines=("md_a PASS", "md_b PASS", "md_c PASS", "SB5_uci293 PASS", "md_zzz PASS"))
    assert any("outside the input" in x and "md_zzz" in x for x in p)


def test_a_hit_id_left_in_the_mix_fails(tmp_path):
    p = check(tmp_path, lines=("md_a PASS", "md_b HIT", "md_c PASS", "SB5_uci293 PASS"))
    assert any("HIT source(s) still in the mix" in x and "md_b" in x for x in p)
    assert not any("without a PASS line" in x for x in p)


def test_a_hit_id_that_is_not_in_the_mix_is_fine(tmp_path):
    assert check(tmp_path, lines=("md_a PASS", "md_b PASS", "md_c HIT", "SB5_uci293 PASS")) == []     # md_c was removed by --remove-sources


def test_an_sb5_hit_left_in_the_mix_fails(tmp_path):
    p = check(tmp_path, lines=("md_a PASS", "md_b PASS", "md_c PASS", "SB5_uci293 HIT"))
    assert any("SB5_uci293" in x and "HIT source(s) still in the mix" in x for x in p)


def test_a_gated_source_not_in_the_input_fails(tmp_path):
    p = check(tmp_path, mix_sources=("c2_md_a", "c2_md_q", "gd_x"), input_ids=("md_a", "md_c"), lines=("md_a PASS", "md_c PASS"))
    assert any("not in the 8.5 input" in x and "md_q" in x for x in p)
    p = check(sub(tmp_path, "y"), mix_sources=("c2_sb5", "gd_x"), input_ids=("md_a",), lines=("md_a PASS",))
    assert any("not in the 8.5 input" in x and "SB5_uci293" in x for x in p)


def test_a_mix_source_whose_line_is_not_a_pass_fails_and_a_removed_source_does_not_matter(tmp_path):
    # md_c is in the input but not in the mix and has a PASS line: fine. A source only in the input, with a HIT: fine (removed).
    assert check(tmp_path, mix_sources=("c2_md_a", "gd_x"), lines=("md_a PASS", "md_b HIT", "md_c PASS", "SB5_uci293 HIT")) == []


def test_the_id_fold_in_the_input_is_by_the_hash_suffix(tmp_path):
    assert check(tmp_path, input_ids=("md_a#1", "md_a#2", "md_b", "md_c", "SB5_uci293#x"), lines=("md_a PASS", "md_b PASS", "md_c PASS", "SB5_uci293 PASS")) == []


def test_a_bad_input_file_fails(tmp_path):
    mix, d = make(tmp_path)
    (d / IN).write_text("{not json")
    relog(d)
    assert "not readable" in pf.check_a61_85(mix, d)[0][0]


# ---- run(): no flag clears the check ---------------------------------------------------------------------------------------
@pytest.mark.parametrize("flags", [[], ["--ack-pending"], ["--offline"], ["--ack-pending", "--offline"]])
def test_neither_ack_pending_nor_offline_clears_the_check(tmp_path, monkeypatch, flags):
    mix_dir = tmp_path / "mix"
    mix_dir.mkdir()
    (mix_dir / "c2_train.jsonl").write_text(row(1, "c2_md_a") + "\n")
    (mix_dir / "c2_mix_manifest.json").write_text("{}")
    (mix_dir / "fill.json").write_text("{}")
    monkeypatch.setattr(pf, "MIX_DIR", mix_dir)
    monkeypatch.setattr(pf, "MANIFEST", mix_dir / "c2_mix_manifest.json")
    monkeypatch.setattr(pf, "FILL", mix_dir / "fill.json")
    monkeypatch.setattr(pf, "LOGS", tmp_path / "logs")
    monkeypatch.setattr(cc, "LOGS", tmp_path / "cclogs")
    monkeypatch.setattr(pf, "A61_DIR", tmp_path / "no_such_di_train")               # no final-run file at all
    rc = pf.run(flags, sh=NoModal(), bill=lambda p: {"credit_left": 100.0, "metered": 0.0})
    rec = json.loads((tmp_path / "logs" / "c2_check_preflight.json").read_text())
    assert rc != 0 and rec["decision"] != "GO" and any("a61_85" in x and "missing" in x for x in rec["problems"]), rec["problems"]
    # the same run with a clean final-run record has no a61_85 problem (other problems remain: this is a fixture, not a GO)
    mix, d = make(sub(tmp_path, "ok"))
    monkeypatch.setattr(pf, "A61_DIR", d)
    (mix_dir / "c2_train.jsonl").write_text(row(1, "c2_md_a") + "\n")
    (d / RES).write_text("md_a PASS\nmd_b PASS\nmd_c PASS\nSB5_uci293 PASS\n")
    relog(d)
    pf.run(flags, sh=NoModal(), bill=lambda p: {"credit_left": 100.0, "metered": 0.0})
    rec = json.loads((tmp_path / "logs" / "c2_check_preflight.json").read_text())
    assert not any("a61_85" in x for x in rec["problems"]), rec["problems"]
    assert rec["a61_85"]["gated_in_mix"] == ["md_a"]


class NoModal:
    def modal(self, profile, args, timeout=120):
        assert profile in cc.PROFILES
        return 1, ""


# ---- c2_tmax.json guard, credit coverage -------------------------------------------------------------------------------------
@pytest.mark.parametrize("rec,ok", [
    ({"t_max": 22.0, "cap_total": 40.0, "formula": "min(34, 32 - spend to date, live credit - 8)"}, True),
    ({"t_max": 22.0, "cap_total": 45.0, "formula": "min(34, 32 - spend to date, live credit - 8)"}, False),
    ({"t_max": 22.0, "cap_total": 40.0, "formula": "min(39, 37 - spend to date)"}, False),
    ({"t_max": 22.0, "cap_total": 45.0, "formula": "min(39, 37 - spend to date)"}, False),
    ({"t_max": 22.0}, False), ({"t_max": 22.0, "cap_total": 40, "formula": "min(34, 32 - spend to date)"}, False),
])
def test_c2_tmax_json_with_another_cap_or_formula_fails(tmp_path, rec, ok):
    f = tmp_path / "c2_tmax.json"
    assert pf.tmax_record_problems(f) == []                                                  # no record: nothing to say
    f.write_text(json.dumps(rec))
    assert (pf.tmax_record_problems(f) == []) is ok
    if not ok:
        assert all("c2_tmax.json" in x for x in pf.tmax_record_problems(f))
    f.write_text("{bad")
    assert pf.tmax_record_problems(f) and pf.tmax_record_problems(f)[0].endswith("not readable JSON")
    f.write_text("[]")
    assert pf.tmax_record_problems(f)


def test_free_credit_must_cover_t_max_and_the_later_lines():
    info = {"mahadikarya2": {"credit_left": 19.0}, "mahadikarya3": {"credit_left": 13.0}}          # usable 30
    p, ci = pf.credit_problems(info, 22.0)
    assert p == [] and ci["covers_t_max"] and ci["covers_t_max_and_later_lines"] and ci["free_credit_usable_usd"] == 30.0
    p, ci = pf.credit_problems(info, 22.01)                                                      # rounding of the fit is tolerated
    assert p == [] and ci["covers_t_max_and_later_lines"]
    p, ci = pf.credit_problems(info, 23.0)                                                       # covers T_max, not the later lines $8
    assert len(p) == 1 and "later lines" in p[0] and ci["covers_t_max"] and not ci["covers_t_max_and_later_lines"]
    p, ci = pf.credit_problems(info, 31.0)
    assert len(p) == 1 and "does not cover T_max" in p[0] and not ci["covers_t_max"]


def test_the_accounts_check_covers_only_the_two_relay_accounts(tmp_path):
    seen = []

    class Sh:
        def modal(self, profile, args, timeout=120):
            seen.append(profile)
            if args[:2] == ["profile", "list"]:
                return 0, "mahadikarya2 mahadikarya3 jaypatil-duke"
            if args[:2] == ["app", "list"]:
                return 0, "[]"
            if args[:3] == ["volume", "ls", "opendecide"] and args[3].endswith("_init"):
                return 0, "adapter_model.safetensors"
            return 1, "not found"
    p, info, base = pf.check_accounts(Sh(), lambda pr: {"credit_left": 10.0, "metered": 1.0})
    assert p == [] and set(seen) == {"mahadikarya2", "mahadikarya3"} and list(info) == ["mahadikarya2", "mahadikarya3"]
