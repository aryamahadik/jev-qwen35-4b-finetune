"""CPU tests of c_build/decontam_g13.py (G13, spec 7; RUNBOOK B). Tiny synthetic rows only; no real eval set is read."""
import json
import sys
from pathlib import Path

import pytest

CB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CB))
import decontam_g13 as g  # noqa: E402

LONG = ("the quarterly ledger of the harbor authority lists eleven dredging contracts awarded "
        "between march and october with the largest going to a firm from the northern docks")


def row(i, call, state, instr="Read the record and answer the question below carefully.", opts=("yes", "no")):
    return {"id": f"r{i}", "call_id": call, "source": "c_test", "state": state, "instructions": instr,
            "options": list(opts), "card": None}


def write_jsonl(p: Path, rows):
    p.write_text("".join(json.dumps(r) + "\n" for r in rows))
    return p


def tg(name, path, **kw):
    return g.target(name, [f"abs:{path}"], **kw)


@pytest.fixture
def setup(tmp_path):
    train = [
        row(0, "u0", LONG),                                                          # exact_full vs eval A
        row(1, "u0", "a second row of the same unit with unrelated filler words here"),  # same unit -> dropped too
        row(2, "u1", "intro words first. " + "Mariners counted nine gulls on the pier at dawn today."),  # exact_seg
        row(3, "u2", "prefix text " + "the violet kettle hummed beside the open window all afternoon" + " suffix"),
        row(4, "u3", "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi"),  # ngram10
        row(5, "u4", "completely different clean text about gardening tools and soil acidity levels in spring"),
        row(6, "u5", "Short Item", opts=("yes", "no")),                               # exact_short (state)
        row(7, "u6", "something else entirely with many words in it for the test", opts=("Blue Moon", "no")),
        row(8, "u7", "| name | year |\n|---|---|\n| ada | 1843 |\n| alan | 1936 |"),       # table
    ]
    tp = write_jsonl(tmp_path / "train.jsonl", train)
    ev = [
        {"id": "e0", "state": LONG, "instructions": "x", "options": ["a", "b"]},
        {"id": "e1", "state": "Mariners counted nine gulls on the pier at dawn today. Then other text follows here.",
         "options": []},
        {"id": "e2", "state": "the violet kettle hummed beside the open window all afternoon", "options": []},
        {"id": "e3", "state": "zz alpha beta gamma delta epsilon zeta eta theta iota kappa yy qq rr ss", "options": []},
        {"id": "e4", "state": "short item", "options": []},
        {"id": "e5", "state": "blue moon", "options": []},                          # equals only a training OPTION
        {"id": "e6", "state": "| name | year |\n|---|---|\n| alan | 1936 |\n| ada | 1843 |", "options": []},
    ]
    ep = write_jsonl(tmp_path / "eval.jsonl", ev)
    return tmp_path, tp, ep


def scan(setup, tgs=None, units_extra=()):
    tmp, tp, ep = setup
    units = g.train_units(tp) + list(units_extra)
    tgs = tgs or [tg("ev", ep, tables=True, blind=True)]
    return g.run("T", units, {"train.jsonl": "x"}, {}, tgs, tmp / "out", cosine=tmp / "none.json")


def test_methods_fire_and_whole_unit_drops(setup):
    rec = scan(setup)
    m = rec["counts_by_eval_and_method"]["ev"]
    assert m["exact_full"]["units"] >= 1 and m["exact_seg"]["units"] >= 1
    assert m["substring"]["units"] >= 1 and m["ngram10"]["units"] >= 1
    assert m["exact_short"]["units"] == 1 and m["table"]["units"] == 1
    assert "r0" in rec["drop_ids"] and "r1" in rec["drop_ids"]          # the whole call_id unit
    assert {"r2", "r3", "r4", "r6", "r8"} <= set(rec["drop_ids"])
    assert "r5" not in rec["drop_ids"]
    assert "r7" not in rec["drop_ids"]                                    # a short eval item vs a training option
    assert rec["short_items"]["ev"] == 2


def test_no_eval_text_in_output(setup):
    rec = scan(setup)
    blob = json.dumps(rec).lower()
    for w in ("dredging", "mariners", "kettle", "omicron", "1843"):
        assert w not in blob
    out = (setup[0] / "out/T.json").read_text().lower()
    assert "dredging" not in out and "drop_ids" in out


def test_tulu_and_minhash(setup, tmp_path):
    base = ("one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
            "seventeen eighteen nineteen twenty")
    near = base.replace("seventeen", "zzz")
    p = write_jsonl(tmp_path / "e2.jsonl", [{"id": "n", "state": near, "options": []}])
    tmp, tp, _ = setup
    units = g.train_units(write_jsonl(tmp / "t2.jsonl", [row(0, "u0", base)]))
    rec = g.run("T2", units, {}, {}, [tg("ev2", p)], tmp / "out", cosine=tmp / "none.json")
    m = rec["counts_by_eval_and_method"]["ev2"]
    assert m["tulu8"]["units"] == 1 and m["ngram10"]["units"] == 1
    # minhash: identical 5-gram sets except one word -> Jaccard below 0.8 here; an exact copy passes
    p2 = write_jsonl(tmp_path / "e3.jsonl", [{"id": "c", "state": base + " extra", "options": []}])
    rec = g.run("T3", units, {}, {}, [tg("ev3", p2)], tmp / "out", cosine=tmp / "none.json")
    assert rec["counts_by_eval_and_method"]["ev3"]["minhash"]["units"] == 1


def test_restricted_methods_and_pending_owner(setup):
    tmp, tp, ep = setup
    tgs = [tg("posts", ep, methods=("exact", "substring")),
           g.target("ohs3", [], status="pending_owner", note="owner"),
           g.target("nothere", ["abs:" + str(tmp / "missing.jsonl")])]
    rec = scan(setup, tgs)
    m = rec["counts_by_eval_and_method"]["posts"]
    assert "ngram10" not in m and "minhash" not in m and "substring" in m
    assert rec["complete"] is False
    why = " ".join(rec["incomplete_why"])
    assert "ohs3" in why and "nothere" in why and "embed" in why
    assert rec["targets"]["ohs3"]["status"] == "pending_owner" and rec["targets"]["nothere"]["status"] == "missing"


def test_seed_hits_are_not_drop_ids(setup):
    seed = {"key": "seed:gen/x.py#0", "rows": [], "source": "seed:gen/x.py", "seed": True,
            "texts": [("seed", "the violet kettle hummed beside the open window all afternoon")]}
    rec = scan(setup, units_extra=[seed])
    assert rec["seeds_clean"] is False and rec["seed_hit_locs"] == ["seed:gen/x.py#0"]
    assert all(not d.startswith("seed:") for d in rec["drop_ids"])


def test_py_literals_skip_docstrings():
    src = '"""module doc with many words in it here"""\ndef f():\n    """fn doc"""\n    return f"Answer {x} now please"\nT = "a template line"\n'
    lit = g.py_literals(src)
    assert "a template line" in lit and not any("module doc" in x for x in lit) and "fn doc" not in lit


@pytest.mark.parametrize("rel,ok", [
    ("opendecide-data/lean/data/ohs3.jsonl", False), ("opendecide-data/lean/data/ohs3_parts/a.jsonl", False),
    ("opendecide-data/lean/ohs3/x.json", False), ("bench/longbench_v2/a.jsonl", False),
    ("opendecide-data/lean/sealed_nd/suite_v2.jsonl", False), ("opendecide-data/lean/preds_ohs/x.jsonl", False),
    ("bench/jevbench_v154/results/x.jsonl", False), ("bench/runs/jev_p1/a.jsonl", False),
    ("opendecide-data/lean/logs/jev_ohs.log", False), ("bench/external_quarantine/ejs5/public_raw.json", False),
    ("bench/jevbench/datasets/public/easy.jsonl", True), ("bench/splits/jevbench_all.jsonl", True),
    ("bench/external_quarantine/ejs5/ejs5_rows.jsonl", True), ("opendecide-data/lean/data/dev_nc.jsonl", True),
])
def test_allowed(rel, ok):
    assert g.allowed(g.REPO / rel) is ok


def test_jev_keys_never_read():
    assert list(g.leaves({"state": "keep me", "jev_recorded_p_yes": "secret words here", "Jev_x": ["no"]})) == ["keep me"]


def test_log_problems(tmp_path, monkeypatch):
    monkeypatch.setattr(g, "LEAN", tmp_path)
    monkeypatch.setattr(g, "eval_stale", lambda d: None)      # the eval-side check: test_decontam_g13_a25
    (tmp_path / "c.jsonl").write_text("{}\n")
    good = {"set": "F3", "drop_ids": [], "complete": True, "seeds_clean": True,
            "methods": g.methods_desc(g.targets(), True, {"threshold": 0.95, "model": "m"}),
            "rules": {"table_hash": "header + cell set; every public-2 container"},
            "inputs_sha256": {"train": {"c.jsonl": g.sha256_file(tmp_path / "c.jsonl")}, "seeds": {}}}
    (tmp_path / "F3.json").write_text(json.dumps({**good, "methods": {}}))
    assert "not run in this log" in g.log_problems(["F3"], tmp_path)[0]
    (tmp_path / "F3.json").write_text(json.dumps(good))
    assert g.log_problems(["F3"], tmp_path) == []
    assert "no logs" in g.log_problems(["F6"], tmp_path)[0]
    (tmp_path / "c.jsonl").write_text("{}\n{}\n")
    assert "stale" in g.log_problems(["F3"], tmp_path)[0]
    bad = {**good, "complete": False, "incomplete_why": ["ohs3: pending"], "inputs_sha256": {}}
    (tmp_path / "F3.json").write_text(json.dumps(bad))
    assert "incomplete" in g.log_problems(["F3"], tmp_path)[0]
    fin = {**good, "set": "final_mix_r1", "drop_ids": ["r1"], "inputs_sha256": {}}
    (tmp_path / "final_mix_r1.json").write_text(json.dumps(fin))
    assert any("still has 1 hits" in x for x in g.log_problems(["final_mix_r1"], tmp_path))


def test_mixer_reads_drop_ids(setup):
    rec = scan(setup)
    assert isinstance(rec["drop_ids"], list) and rec["drop_ids"] == sorted(rec["drop_ids"])
