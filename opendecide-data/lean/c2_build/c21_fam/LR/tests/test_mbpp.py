import gzip
import json

import lr_common as lc
import lr_testlib as T
import mbpp as M


def records(n=20):
    out = []
    for i in range(n):
        out.append({"task_id": 601 + i, "text": "Write a function %d." % i,
                    "code": "def f%d(a, b):\r\n    if a > b:\r\n        return a + %d\r\n    return b - 1" % (i, i + 2),
                    "test_list": ["assert f%d(5, 3) == %d" % (i, 5 + i + 2), "assert f%d(1, 3) == 2" % i, "assert f%d(9, 2) == %d" % (i, 9 + i + 2)],
                    "test_setup_code": "", "challenge_test_list": [], "_src_line": "mbpp:%d" % (601 + i)})
    return out


def fake_exec(code, setup, test):
    """A pure-text oracle standing in for the sandbox (CPU tests only; it never runs dataset code): a mutant 'passes'
    only when it equals the original text; the mutator always changes the text, so mutants 'fail'."""
    orig = {("def f%d(a, b):\n    if a > b:\n        return a + %d\n    return b - 1" % (i, i + 2)) for i in range(40)}
    return code in orig


def test_rows_gold_from_exec_balanced():
    m = M.Mapper(T.pools_for(M.Mapper), seed=1, exec_fn=fake_exec)
    rows = m.map_records(records(20), cap=20)
    T.check_rows(rows, m, expect_kind=("yesno",), min_rows=20, )
    rep = T.check_set_report(rows, yes_no=True)
    assert rep["R7_pass"] and rep["yes_rate"] == 0.5
    for r in rows:
        assert r["answer_text"] == ("No" if r["extra"]["variant"] == "orig" else "Yes")
        assert r["context"].count("Stated test:") == 1 and "Function:\n" in r["context"]
    assert all("\r" not in r["context"] and "\t" not in r["context"] for r in rows)
    assert len({r["extra"]["task_id"] for r in rows if r["answer_text"] == "Yes"}) == len([r for r in rows if r["answer_text"] == "Yes"])


def test_no_exec_hook_means_no_rows():
    m = M.Mapper(T.pools_for(M.Mapper), seed=1)
    assert m.map_records(records(5), cap=10) == []
    assert m.drops.c["tfail_hooks_missing"] > 0


def test_human_solution_failing_and_exec_errors_drop():
    bad = lambda code, setup, test: False
    m = M.Mapper(T.pools_for(M.Mapper), seed=1, exec_fn=bad)
    rows = m.map_records(records(3), cap=10)
    assert all(r["extra"]["variant"] == "mutant" and r["answer_text"] == "Yes" for r in rows)
    assert m.drops.c["human_solution_fails_own_test"] == 3
    m2 = M.Mapper(T.pools_for(M.Mapper), seed=1, exec_fn=lambda c, s, t: None)
    assert m2.map_records(records(3), cap=10) == [] and m2.drops.c["exec_error_or_timeout"] > 0


def test_r4_second_execution_must_agree():
    calls = {"n": 0}

    def flaky(code, setup, test):
        calls["n"] += 1
        return calls["n"] % 2 == 1          # a different answer on every second call
    m = M.Mapper(T.pools_for(M.Mapper), seed=1, exec_fn=flaky)
    rows = m.map_records(records(6), cap=20)
    assert all(r["answer_text"] in ("Yes", "No") for r in rows)
    assert m.drops.c.get("R4_gold_mismatch", 0) > 0


def test_simple_mutants_deterministic_distinct_text():
    code = M.normalise_code(records(1)[0]["code"])
    a, b = M.simple_mutants(code, 4, 0), M.simple_mutants(code, 4, 0)
    assert a == b and len(a) == 4 and len(set(a)) == 4 and code not in a


def test_setup_code_and_budget():
    m = M.Mapper(T.pools_for(M.Mapper), seed=1, exec_fn=fake_exec)
    r = records(1)[0]
    r["test_setup_code"] = "import math"
    rows = m.map_records([r], cap=4)
    assert rows and rows[0]["context"].startswith("Setup code:\nimport math")
    m2 = M.Mapper(T.pools_for(M.Mapper), seed=1, exec_fn=fake_exec)
    big = records(1)[0]
    big["code"] = "def f0(a, b):\n" + "\n".join("    x%d = %d + a * b" % (j, j) for j in range(400))
    assert m2.map_records([big], cap=4) == [] and m2.drops.c["code_over_budget"] >= 1


def test_reader(tmp_path):
    with gzip.open(str(tmp_path / "train.jsonl.gz"), "wt") as f:
        f.write(json.dumps({k: v for k, v in records(1)[0].items() if k != "_src_line"}) + "\n")
    assert [g["task_id"] for g in M.read_train(str(tmp_path))] == [601]


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(M.Mapper)
