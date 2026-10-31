import pyarrow as pa
import pyarrow.parquet as pq

import lr_common as lc
import lr_testlib as T
import boardgameqa as B


def records(n=30):
    labs = ["proved", "disproved", "unknown"]
    cfgs = ["Main-depth1", "ManyDistractors-depth2", "Main-depth3"]
    return [{"example": "A few players are playing a boardgame. The cat eats the food of wolf number %d. Rule1: if X then Y. "
                        "Based on the game state and the rules and preferences, does the cat respect the fish number %d?" % (i, i),
             "label": labs[i % 3], "config": cfgs[i % 3 if i % 2 else (i // 3) % 3], "_src_line": "bgqa:%d" % i} for i in range(n)]


def test_rows_thirds_and_abstain_flag(monkeypatch):
    m = B.Mapper(T.pools_for(B.Mapper), seed=1)
    rows = m.map_records(records(30), cap=30)
    T.check_rows(rows, m, expect_kind=("choice",), min_rows=30)
    cnt = {o: sum(r["answer_text"] == o for r in rows) for o in B.OPTIONS}
    assert set(cnt.values()) == {10}
    for r in rows:
        assert r["k"] == 3 and r["flags"]["native_abstain_label"] == (r["answer_text"] == "Unknown")
        i = int(r["source_row_id"].split(":")[1])
        assert r["answer_text"] == B.OPTIONS[i % 3]
    assert T.check_set_report(rows)["R5_position_pass"]


def test_over_cap_example_dropped_and_proof_never_read(tmp_path):
    m = B.Mapper(T.pools_for(B.Mapper), seed=1)
    long = dict(records(1)[0], example="word " * 2500)
    assert m.map_records([long]) == [] and m.drops.c["R6_example_over_cap_precheck"] == 1
    pq.write_table(pa.table({"example": ["e0"], "label": ["proved"], "config": ["Main-depth1"], "proof": ["SECRET PROOF"], "theory": ["t"], "goal": ["g"]}),
                   str(tmp_path / "train-00000-of-00001-x.parquet"))
    pq.write_table(pa.table({"example": ["HELD"], "label": ["proved"], "config": ["c"]}), str(tmp_path / "valid-00000-of-00001-y.parquet"))
    got = list(B.read_train(str(tmp_path)))
    assert got == [{"example": "e0", "label": "proved", "config": "Main-depth1", "_src_line": "bgqa:0"}]


def test_r4_and_unknown_label_dropped():
    m = B.Mapper(T.pools_for(B.Mapper), seed=1)
    bad = dict(records(1)[0], label="maybe")
    assert m.map_records([bad]) == []
    m.independent_gold = lambda s, c: "?"
    assert m.map_records(records(6)) == []


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(B.Mapper)
