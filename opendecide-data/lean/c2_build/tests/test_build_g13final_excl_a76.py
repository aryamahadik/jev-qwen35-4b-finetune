import sys, json, hashlib
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "zed_orch" / "a76"))
sys.dont_write_bytecode = True
import build_g13final_excl as b  # noqa: E402


def log(**kw):
    d = {"set": "c2_final", "run": "final", "block": "final", "complete": True, "incomplete_why": [], "rows": 5, "units": 4,
         "drop_ids": ["a", "b", "c", "d"],
         "drop_ids_by_class": {"binding": ["c", "a", "a"], "ohsac_report_only": ["b", "d"], "units": [], "capture": []}}
    d.update(kw)
    return d


def test_copies_only_binding_sorted_deduped():
    r = b.build(log(), 3)
    assert r["drop_ids"] == ["a", "c"]
    assert r["drop_ids_sha256"] == hashlib.sha256(b"a\nc").hexdigest()
    assert r["complete"] is True and r["incomplete_why"] == "" and r["set"] == "a76_excl_g13final_3" and r["tool"] == b.TOOL
    assert "b" not in r["drop_ids"] and "d" not in r["drop_ids"]
    assert r["counts"]["binding_ids"] == 2 and r["counts"]["binding_ids_in_log"] == 3


@pytest.mark.parametrize("kw", [{"complete": False}, {"complete": None}, {"incomplete_why": ["x"]}, {"incomplete_why": "why"}])
def test_refuses_incomplete(kw):
    with pytest.raises(ValueError):
        b.build(log(**kw), 3)


def test_refuses_missing_class():
    d = log(); del d["drop_ids_by_class"]
    with pytest.raises(ValueError):
        b.build(d, 3)
    with pytest.raises(ValueError):
        b.build(log(drop_ids_by_class={"ohsac_report_only": ["b"]}), 3)


def test_refuses_non_final():
    with pytest.raises(ValueError):
        b.build(log(run="dev", block="dev"), 3)


def test_empty_binding_ok():
    r = b.build(log(drop_ids_by_class={"binding": [], "ohsac_report_only": ["b"]}), 4)
    assert r["drop_ids"] == [] and r["set"] == "a76_excl_g13final_4"


def test_cli_writes_and_prints_no_ids(tmp_path, capsys):
    lp = tmp_path / "l.json"; lp.write_text(json.dumps(log()))
    out = tmp_path / "o.json"
    assert b.main(["--log", str(lp), "--n", "3", "--out", str(out)]) == 0
    o = json.loads(out.read_text())
    assert o["drop_ids"] == ["a", "c"]
    txt = capsys.readouterr().out
    assert "binding ids 2" in txt and "sha256" in txt
