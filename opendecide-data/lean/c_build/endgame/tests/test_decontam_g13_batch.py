"""CPU tests of c_build/decontam_g13_batch.py: one eval pass for several sets gives, per set, the same record as a lone
decontam_g13.run. Tiny synthetic rows only; no real eval set is read."""
import json
import sys
from pathlib import Path

import pytest

CB = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CB))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import decontam_g13 as g  # noqa: E402
import decontam_g13_batch as b  # noqa: E402
from test_decontam_g13 import LONG, row, tg, write_jsonl  # noqa: E402

KETTLE = "the violet kettle hummed beside the open window all afternoon"
VOLATILE = ("wall_s", "unix", "batch")


@pytest.fixture
def two_sets(tmp_path):
    a = [row(0, "u0", LONG), row(1, "u0", "a second row of the same unit with unrelated filler words here"),
         row(2, "u1", "intro words first. Mariners counted nine gulls on the pier at dawn today."),
         row(3, "u2", "alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi"),
         row(4, "u3", "something else entirely with many words in it for the test", opts=("Blue Moon", "no"))]
    bb = [{**row(10, "v0", LONG), "id": "b0"},                                   # the same text as set A's u0
          {**row(11, "v1", "prefix text " + KETTLE + " suffix"), "id": "b1"},
          {**row(12, "v2", "completely different clean text about gardening tools and soil acidity levels"), "id": "b2"},
          {**row(13, "v3", "| name | year |\n|---|---|\n| ada | 1843 |\n| alan | 1936 |"), "id": "b3"},
          {**row(14, "v4", "Short Item"), "id": "b4"}]
    ta, tb = write_jsonl(tmp_path / "a.jsonl", a), write_jsonl(tmp_path / "b.jsonl", bb)
    ev = [{"id": "e0", "state": LONG, "instructions": "x", "options": ["a", "b"]},
          {"id": "e1", "state": "Mariners counted nine gulls on the pier at dawn today. Then other text follows here.",
           "options": []},
          {"id": "e2", "state": KETTLE, "options": []},
          {"id": "e3", "state": "zz alpha beta gamma delta epsilon zeta eta theta iota kappa yy qq rr ss", "options": []},
          {"id": "e4", "state": "short item", "options": []},
          {"id": "e5", "state": "blue moon", "options": []},
          {"id": "e6", "state": "| name | year |\n|---|---|\n| alan | 1936 |\n| ada | 1843 |", "options": []}]
    ep = write_jsonl(tmp_path / "eval.jsonl", ev)
    seed = {"key": "seed:gen/x.py#0", "rows": [], "source": "seed:gen/x.py", "seed": True, "texts": [("seed", KETTLE)]}

    def sets():
        return {"A": (g.train_units(ta), {"a.jsonl": "sa"}, {}),
                "B": (g.train_units(tb) + [dict(seed)], {"b.jsonl": "sb"}, {"gen/x.py": "sx"})}
    return tmp_path, sets, [tg("ev", ep, tables=True, blind=True)]


def four(sets):
    return {n: (*v, None) for n, v in sets.items()}


def strip(rec):
    return {k: v for k, v in rec.items() if k not in VOLATILE}


def test_batch_equals_lone_runs(two_sets):
    tmp, sets, tgs = two_sets
    none = tmp / "none.json"
    lone = {n: g.run(n, us, ts, ss, tgs, tmp / f"lone_{n}", cosine=none, side=False)
            for n, (us, ts, ss) in sets().items()}
    multi = g.run_sets(four(sets()), tgs, tmp / "multi", cosine=none, side=False)
    for n in ("A", "B"):
        assert strip(multi[n]) == strip(lone[n]), n
        assert json.loads((tmp / "multi" / f"{n}.json").read_text())["batch"]["sets"] == ["A", "B"]
    assert multi["A"]["drop_ids"] == ["r0", "r1", "r2", "r3"]     # u0 (both rows), u1 seg, u2 ngram10; not the option
    assert multi["B"]["drop_ids"] == ["b0", "b1", "b3", "b4"]     # shared LONG text, substring, table, short state
    assert multi["B"]["seeds_clean"] is False and multi["A"]["seeds_clean"] is True


def test_no_eval_text_in_batch_logs(two_sets):
    tmp, sets, tgs = two_sets
    g.run_sets(four(sets()), tgs, tmp / "multi", cosine=tmp / "none.json", side=False)
    blob = "".join(p.read_text() for p in (tmp / "multi").glob("*.json")).lower()
    assert "mariners" not in blob and "violet" not in blob and "harbor" not in blob


def test_threshold_file_without_model_is_not_used(two_sets):
    """The batch no longer refuses a fixed threshold (the top-5 is per set, test_decontam_g13_a25); a threshold file
    without a model is not a fixed threshold: method 5 is not run and every log stays incomplete."""
    tmp, sets, tgs = two_sets
    cos = tmp / "thr.json"
    cos.write_text(json.dumps({"threshold": 0.9}))
    recs = g.run_sets(four(sets()), tgs, tmp / "multi", cosine=cos, side=False)
    assert all(not r["complete"] and any(w.startswith("embed (method 5)") for w in r["incomplete_why"])
               for r in recs.values())


def test_cli_rejects_unknown_set():
    with pytest.raises(SystemExit):
        b.main(["--sets", "F99"])
