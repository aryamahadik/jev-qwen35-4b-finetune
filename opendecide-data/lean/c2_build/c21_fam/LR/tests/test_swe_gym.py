import gzip
import json

import lr_common as lc
import lr_testlib as T
import swe_gym as S


def diff(path, n):
    return "diff --git a/%s b/%s\nindex 1111111..2222222 100644\n--- a/%s\n+++ b/%s\n@@ -1,3 +1,3 @@\n context line %d\n-old line %d\n+new line %d\n" % (path, path, path, path, n, n, n)


def records(n=24):
    out = []
    for i in range(n):
        repo = ["owner/alpha", "owner/beta"][i % 2]
        src = "pkg/mod%d/core%d.py" % (i % 6, i)
        tst = "tests/test_mod%d/test_core%d.py" % (i % 6, i)
        out.append({"instance_id": "%s-%d" % (repo.replace("/", "__"), 1000 + i), "repo": repo, "base_commit": "abc%d" % i, "version": "1.%d" % (i % 3),
                    "created_at": "2024-01-01", "patch": diff(src, i), "test_patch": diff(tst, i),
                    "FAIL_TO_PASS": ["tests/test_mod%d/test_core%d.py::test_it_%d" % (i % 6, i, j) for j in range(3)],
                    "_src_line": "swegym:%s-%d" % (repo.replace("/", "__"), 1000 + i)})
    return out


def test_rows_gold_forms_and_k():
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    rows = m.map_records(records(24), cap=40)
    T.check_rows(rows, m, expect_kind=("choice",), min_rows=30)
    assert {r["form"] for r in rows} == {S.F_FIX, S.F_TEST}
    for r in rows:
        i = int(r["source_row_id"].rsplit("-", 1)[1]) - 1000
        want = ("pkg/mod%d/core%d.py" if r["form"] == S.F_FIX else "tests/test_mod%d/test_core%d.py") % (i % 6, i)
        assert r["answer_text"] == want and 2 <= r["k"] <= 8
        # distractors are paths from the SAME repo only
        repo_tag = r["extra"]["instance"].split("-")[0]
        for o in r["options"]:
            if o != want:
                j = int(o.split("core")[1].split(".")[0])
                assert records(24)[j]["repo"].replace("/", "__") == repo_tag
    assert T.check_set_report(rows)["R5_position_pass"] or len(rows) < 100


def test_no_issue_text_or_execution_lists_in_rows():
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    recs = records(12)
    for r in recs:
        r["problem_statement"] = "SECRET ISSUE TEXT"
        r["PASS_TO_PASS"] = ["SECRET_P2P"]
    rows = m.map_records(recs, cap=20)
    assert rows and all("SECRET" not in lc.render_plain(r) for r in rows)


def test_drops_multi_file_small_pool_and_budget():
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    recs = records(6)
    multi = dict(recs[0], patch=recs[0]["patch"] + diff("pkg/extra.py", 9))
    rows = m.map_records([multi] + recs[1:], cap=40)
    assert m.drops.c["patch_not_single_file"] >= 1 and m.drops.c["pool_too_small"] >= 1
    m2 = S.Mapper(T.pools_for(S.Mapper), seed=1)
    recs2 = records(24)
    recs2[0]["patch"] = diff("pkg/mod0/core0.py", 0) + "\n".join("+added line %d with several words in it" % j for j in range(400))
    m2.map_records(recs2, cap=60)
    assert m2.drops.c["patch_over_budget"] == 1


def test_r4_and_reader(tmp_path):
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    m.independent_gold = lambda s, c: "?"
    assert m.map_records(records(12), cap=20) == []
    with gzip.open(str(tmp_path / "train.jsonl.gz"), "wt") as f:
        f.write(json.dumps({k: v for k, v in records(1)[0].items() if k != "_src_line"}) + "\n")
    assert [g["instance_id"] for g in S.read_train(str(tmp_path))] == ["owner__alpha-1000"]


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(S.Mapper)
