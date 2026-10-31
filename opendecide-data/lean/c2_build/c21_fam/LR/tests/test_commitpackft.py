import gzip
import json

import lr_common as lc
import lr_testlib as T
import commitpackft as M

LANGS = ["Python", "Go", "Java", "Ruby"]


def commit(i, repo, lang="Python", license="mit", subject=None):
    n = i
    old = "\n".join("line %d of file %d" % (j, n) for j in range(30))
    new = old.replace("line 7 of file %d" % n, "line 7 changed in commit %d" % n)
    subjects = ["Fix handling of the null pointer in module %d" % n, "Add retry logic to the network client %d" % n,
                "Remove the deprecated option from the parser %d" % n, "Rename helper functions for clarity in part %d" % n]
    return {"commit": "sha%04d" % i, "old_file": "src/f%d.py" % i, "new_file": "src/f%d.py" % i, "old_contents": old, "new_contents": new,
            "subject": subject or subjects[i % 4], "message": (subject or subjects[i % 4]) + "\n", "lang": lang, "license": license,
            "repos": repo, "_src_line": "cpft:%s:sha%04d:src/f%d.py" % (lang, i, i)}


def records(n=40):
    return [commit(i, "owner/repo%d" % (i % 5), LANGS[i % 4]) for i in range(n)]


def test_rows_balanced_gold_swap_is_same_repo():
    m = M.Mapper(T.pools_for(M.Mapper), seed=1)
    recs = records(40)
    rows = m.map_records(recs, cap=20)
    T.check_rows(rows, m, expect_kind=("yesno",), min_rows=6)
    rep = T.check_set_report(rows, yes_no=True)
    assert rep["R7_pass"] and rep["yes_rate"] == 0.5
    by_commit = {r["commit"]: r for r in recs}
    for r in rows:
        own = by_commit[r["extra"]["pair"].split(":")[2]]
        shown = r["extra"]["shown_subject"]
        if r["answer_text"] == "Yes":
            assert shown == own["subject"]
        else:
            donors = [c for c in recs if c["subject"] == shown]
            assert donors and all(d["repos"] == own["repos"] and d["commit"] != own["commit"] for d in donors)
            assert M.jaccard(own["subject"], shown) < 0.5
        assert "@@" in r["context"] and r["context"].rstrip().endswith(shown)


def test_duplicate_commit_file_rows_are_used_once():
    m = M.Mapper(T.pools_for(M.Mapper), seed=1)
    recs = records(10)
    rows = m.map_records(recs + [dict(recs[0])] + [dict(recs[1])], cap=20)
    assert m.drops.c["duplicate_item"] == 2
    assert len({(r["source_row_id"], r["form"]) for r in rows}) == len(rows)


def test_whitelist_language_and_subject_rules():
    m = M.Mapper(T.pools_for(M.Mapper), seed=1)
    ok = commit(1, "o/r")
    agpl = commit(2, "o/r", license="agpl-3.0")
    md = commit(3, "o/r", lang="Markdown")
    short = commit(4, "o/r", subject="Fix typo")
    rows = m.map_records([ok, agpl, md, short], cap=4)
    assert rows == [] or all(r["extra"]["license"] == "mit" for r in rows)
    assert m.drops.c["licence_not_whitelisted"] == 1 and m.drops.c["excluded_language"] == 1 and m.drops.c["subject_under_4_tokens"] == 1


def test_swap_rules_jaccard_and_diff_budget():
    m = M.Mapper(T.pools_for(M.Mapper), seed=1)
    a = commit(1, "o/r", subject="Fix handling of the null pointer in module")
    b = dict(commit(2, "o/r", subject="Fix handling of the null pointer in module again"), _role="no", _shown="Fix handling of the null pointer in module")
    b["_src_line"] += "x"
    assert m.build(dict(b, subject="Fix handling of the null pointer in module again"), {}) == [] and m.drops.c["swap_subjects_too_similar"] == 1
    big = commit(3, "o/r")
    big["new_contents"] = "\n".join("completely different text number %d with many words" % j for j in range(380))
    assert m.build(dict(big, _role="yes", _shown=big["subject"]), {}) == [] and m.drops.c["diff_over_budget"] == 1
    huge = commit(4, "o/r")
    huge["old_contents"] = "x" * 30000
    assert m.build(dict(huge, _role="yes", _shown=huge["subject"]), {}) == [] and m.drops.c["file_too_long"] == 1
    same = commit(5, "o/r")
    same["new_contents"] = same["old_contents"]
    assert m.build(dict(same, _role="yes", _shown=same["subject"]), {}) == [] and m.drops.c["empty_diff"] == 1


def test_per_repo_limit_and_r4():
    m = M.Mapper(T.pools_for(M.Mapper), seed=2)
    rows = m.map_records([commit(i, "owner/one", "Python") for i in range(30)], cap=40)
    assert all(sum(1 for r in rows if r["answer_text"] == a) <= 3 for a in ("Yes", "No"))
    m2 = M.Mapper(T.pools_for(M.Mapper), seed=1)
    m2.independent_gold = lambda s, c: "?"
    assert m2.map_records(records(10), cap=6) == []


def test_reader_filters_licence_and_language(tmp_path):
    (tmp_path / "data").mkdir()
    with gzip.open(str(tmp_path / "data" / "Python.jsonl.gz"), "wt") as f:
        for r in (commit(1, "o/r"), commit(2, "o/r", license="isc")):
            f.write(json.dumps({k: v for k, v in r.items() if k != "_src_line"}) + "\n")
    with gzip.open(str(tmp_path / "data" / "markdown.jsonl.gz"), "wt") as f:
        f.write(json.dumps(commit(3, "o/r", lang="Markdown")) + "\n")
    got = list(M.read_train(str(tmp_path)))
    assert [g["commit"] for g in got] == ["sha0001"]


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(M.Mapper)
