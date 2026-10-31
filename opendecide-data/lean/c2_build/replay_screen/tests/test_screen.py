"""pytest for replay_screen/screen.py on fabricated fixtures (no real data, no model).

  ../../../../.venv/bin/python -B -m pytest -q replay_screen/tests/test_screen.py   (from c2_build)
"""
import gzip
import json
import sys
from collections import Counter
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import screen as S  # noqa: E402


def make_rows(n=240):
    rows = []
    for i in range(n):
        src = ("src_yn", "src_choice", "src_long")[i % 3]
        r = {"id": f"t_{src}_{i}", "source": src, "group": f"g:{i}", "role": "q", "soft": False, "attacked": False,
             "unit": f"u{i // 2}" if i < 40 else f"u{i}", "card": "", "options": []}
        if src == "src_choice":
            r |= {"qtype": "choice", "options": ["alpha", "beta", "gamma"], "gold": ["alpha", "beta", "gamma"][i % 3],
                  "state": f"The note number {i} mentions lamp {i}.", "instructions": "Which word fits?"}
        else:
            r |= {"qtype": "noul", "gold": i % 2, "state": f"Report {i}: the lamp {i} was switched on." +
                  (" Extra sentence about weather. " * 120 if src == "src_long" else ""),
                  "instructions": "Was the lamp switched on?"}
        rows.append(r)
    return rows


@pytest.fixture()
def root(tmp_path):
    (tmp_path / "pool").mkdir()
    with gzip.open(tmp_path / "pool" / "population.jsonl.gz", "wt") as f:
        for r in make_rows():
            f.write(json.dumps(r) + "\n")
    return tmp_path


def rows_of(root):
    return S.load_population(root)


def answer_reads(root, wrong=None, abstain=None, skip=None):
    """Fake Haiku: answers the gold, except {reader: set of row ids} wrong / abstain / not answered."""
    wrong, abstain, skip = wrong or {}, abstain or {}, skip or {}
    rows = {r["id"]: r for r in rows_of(root)}
    key = S.jload(root / "reads" / "keys" / "key.json")
    idx = S.jload(root / "reads" / "TASKS.json")
    for t in idx["tasks"]:
        reader = t["reader"]
        qs = {}
        for b in key["readers"][reader]:
            for qid, rid in b["key"].items():
                if b["task_of"][qid] == t["task_id"]:
                    qs[qid] = rid
        out = []
        for qid, rid in qs.items():
            if rid in skip.get(reader, ()):
                continue
            r = rows[rid]
            g = S.gold_text(r)
            if rid in abstain.get(reader, ()):
                a = "abstain"
            elif rid in wrong.get(reader, ()):
                a = ("no" if g == "yes" else "yes") if r["qtype"] == "noul" else [o for o in r["options"] if o != g][0]
            else:
                a = g
            out.append({"qid": qid, "answer": a, "confidence": 0.8})
        Path(t["answer_file"]).write_text(json.dumps(out))


def answer_audit(root, stage, verdict_of):
    key = S.jload(root / stage / "key.json")["key"]
    idx = S.jload(root / stage / "TASKS.json")
    for t in idx["tasks"]:
        out = [{"aid": aid, "verdict": verdict_of(v["row_id"]), "reason": "r"} for aid, v in key.items()
               if v["task_id"] == t["task_id"]]
        Path(t["answer_file"]).write_text(json.dumps(out))


def test_read_tasks_are_gold_free_capped_and_independent(root):
    rows = rows_of(root)
    info = S.build_reads(rows, root, bucket=50)
    idx = S.jload(root / "reads" / "TASKS.json")
    assert info["n_rows"] == len(rows) and info["n_refused"] == 0
    assert idx["max_items_per_file"] <= 50
    assert all(t["n_items"] <= 50 for t in idx["tasks"])
    assert all(Path(t["task_file"]).exists() and t["answer_file"].endswith(".json") for t in idx["tasks"])
    assert {t["allowed_write"][0] for t in idx["tasks"]} == {t["answer_file"] for t in idx["tasks"]}
    key = S.jload(root / "reads" / "keys" / "key.json")
    for reader in ("A", "B"):                                  # every row read exactly once per reader
        seen = Counter(rid for b in key["readers"][reader] for rid in b["key"].values())
        assert set(seen) == {r["id"] for r in rows} and set(seen.values()) == {1}
    a = {rid: qid for b in key["readers"]["A"] for qid, rid in b["key"].items()}
    b = {rid: qid for b in key["readers"]["B"] for qid, rid in b["key"].items()}
    assert all(a[r] != b[r] for r in a)                        # opaque ids differ per reader
    # distinct partitions/orders: the set of rows that share a task file differs between the readers
    task_a = {}
    for bt in key["readers"]["A"]:
        for qid, rid in bt["key"].items():
            task_a[rid] = bt["task_of"][qid]
    task_b = {}
    for bt in key["readers"]["B"]:
        for qid, rid in bt["key"].items():
            task_b[rid] = bt["task_of"][qid]
    mates_a = {frozenset(r for r, t in task_a.items() if t == tid) for tid in set(task_a.values())}
    mates_b = {frozenset(r for r, t in task_b.items() if t == tid) for tid in set(task_b.values())}
    assert mates_a != mates_b
    for t in idx["tasks"]:                                     # gold-free, id-free, contract present
        text = Path(t["task_file"]).read_text()
        assert "human_label" not in text and '"gold"' not in text and "t_src_" not in text
        assert "abstain" in text and '"qid"' in text and "ANSWER FILE" in text
        assert "reads/keys" not in text
    assert not any((root / "reads" / "tasks").glob("*key*"))


def test_flag_rule():
    f = S.is_flagged
    assert f("disagree", "disagree") and f("disagree", "abstain") and f("abstain", "disagree")
    assert f("disagree", "missing") and f("missing", "disagree")
    assert not f("disagree", "agree") and not f("agree", "disagree")
    assert not f("abstain", "abstain") and not f("missing", "missing") and not f("agree", "agree")
    assert not f("abstain", "missing") and not f("agree", "abstain")


def test_read_state_parsing():
    assert S.read_state("yes/no", None, {"answer": " Yes "}, 1) == ("agree", 1)
    assert S.read_state("yes/no", None, {"answer": "no"}, 1) == ("disagree", 0)
    assert S.read_state("yes/no", None, {"answer": "Abstain."}, 1) == ("abstain", None)
    assert S.read_state("choice", ["a1", "b2"], {"answer": "b2"}, "b2") == ("agree", "b2")
    assert S.read_state("choice", ["a1", "b2"], {"answer": "(A)"}, "b2") == ("disagree", "a1")
    assert S.read_state("choice", ["a1", "b2"], {"answer": "zzz"}, "b2")[0] == "missing"
    assert S.read_state("choice", ["a1", "abstain"], {"answer": "abstain"}, "abstain") == ("agree", "abstain")
    assert S.read_state("yes/no", None, {"answer": None}, 1)[0] == "missing"


def test_score_flags_only_double_disputes(root):
    rows = rows_of(root)
    S.build_reads(rows, root, bucket=60)
    ids = [r["id"] for r in rows]
    both_wrong, a_only, b_only, a_wrong_b_abs, b_wrong_a_miss, both_abs = ids[0], ids[1], ids[2], ids[3], ids[4], ids[5]
    answer_reads(root,
                 wrong={"A": {both_wrong, a_only, a_wrong_b_abs}, "B": {both_wrong, b_only, b_wrong_a_miss}},
                 abstain={"B": {a_wrong_b_abs}, "A": {both_abs}},
                 skip={"A": {b_wrong_a_miss}})
    sc = S.score_reads(rows, root)
    assert set(sc["flagged"]) == {both_wrong, a_wrong_b_abs, b_wrong_a_miss}
    assert a_only not in sc["flagged"] and b_only not in sc["flagged"]       # only Haiku (one reader) disputes: stays
    assert both_abs not in sc["flagged"] and both_abs not in sc["agreed"]
    assert b_wrong_a_miss in sc["flagged"] and b_wrong_a_miss not in sc["incomplete"]
    assert set(sc["agreed"]).isdisjoint(sc["flagged"])
    assert set(sc["agreed"]) == set(ids) - {both_wrong, a_only, b_only, a_wrong_b_abs, b_wrong_a_miss, both_abs}
    # a row with a missing read that is not flagged is incomplete (unscreened)
    answer_reads(root, skip={"B": {ids[10]}})
    sc2 = S.score_reads(rows, root)
    assert ids[10] in sc2["incomplete"] and ids[10] not in sc2["agreed"]


def run_pipeline(root, sonnet_called, opus_called):
    rows = rows_of(root)
    S.build_reads(rows, root, bucket=60)
    ids = [r["id"] for r in rows]
    dbl = set(ids[:12])                                          # 12 rows both readers get wrong
    answer_reads(root, wrong={"A": dbl, "B": dbl})
    S.jdump(S.score_reads(rows, root), root / "reads" / "SCORE.json")
    return rows, dbl


def test_adjudicate_confirm_finalize(root):
    rows, dbl = run_pipeline(root, None, None)
    sc = S.jload(root / "reads" / "SCORE.json")
    assert set(sc["flagged"]) == dbl
    info = S.adjudicate(rows, root, n_control=5)
    assert info["flagged"] == 12 and info["controls"] == 15 and set(info["controls_per_source"].values()) == {5}
    idx = S.jload(root / "adjudicate" / "TASKS.json")
    assert all(t["n_items"] <= 50 for t in idx["tasks"])
    mem = S.jload(root / "adjudicate" / "membership.json")
    assert set(mem["controls"]) <= set(sc["agreed"])             # controls are rows both reads agreed with
    text = "".join(Path(t["task_file"]).read_text() for t in idx["tasks"])
    assert "human_label" in text and "read_1" in text and "read_2" in text and "t_src_" not in text
    sonnet = {sorted(dbl)[0]: "wrong_gold", sorted(dbl)[1]: "ambiguous", sorted(dbl)[2]: "gold_ok",
              mem["controls"][0]: "wrong_gold"}
    answer_audit(root, "adjudicate", lambda rid: sonnet.get(rid, "gold_ok"))
    info = S.confirm(rows, root)
    assert info["called"] == 3 and info["first_pass"]["wrong_gold"] == 2
    ctext = "".join(Path(t["task_file"]).read_text() for t in S.jload(root / "confirm" / "TASKS.json")["tasks"])
    assert "first_pass" in ctext
    opus = {sorted(dbl)[0]: "wrong_gold", sorted(dbl)[1]: "gold_ok", mem["controls"][0]: "ambiguous"}
    answer_audit(root, "confirm", lambda rid: opus.get(rid, "gold_ok"))
    out = S.finalize(rows, root)
    deny = S.jload(root / "REPLAY_DENY_A46.json")
    assert set(deny) >= {"set", "drop_ids", "note"} and deny["drop_ids"] == sorted(deny["drop_ids"])
    assert set(deny["drop_ids"]) == {sorted(dbl)[0], mem["controls"][0]}      # Opus-confirmed only; gold_ok overturned
    assert out["confirmed_wrong_gold"] == 1 and out["confirmed_ambiguous"] == 1 and out["overturned_by_opus"] == 1
    # the Sonnet-called row that Opus cleared, and every Haiku-only dispute, stays
    assert sorted(dbl)[1] not in deny["drop_ids"]
    by_unit = {}
    for r in rows:
        by_unit.setdefault(r["unit"], set()).add(r["id"])
    expect = set()
    for rid in deny["drop_ids"]:
        expect |= by_unit[next(r["unit"] for r in rows if r["id"] == rid)]
    assert out["rows_dropped_incl_units"] == len(expect | set(deny["drop_ids"]))
    rep = S.report(rows, root)
    assert rep["totals"]["flagged"] == 12 and rep["totals"]["confirmed"] == 2
    assert rep["totals"]["control_called"] == 1 and (root / "REPORT.md").exists()


def test_finalize_refuses_without_opus_or_with_incomplete_reads(root):
    rows, dbl = run_pipeline(root, None, None)
    S.adjudicate(rows, root, n_control=2)
    answer_audit(root, "adjudicate", lambda rid: "wrong_gold" if rid in dbl else "gold_ok")
    S.confirm(rows, root)
    with pytest.raises(SystemExit):                              # no Opus answers yet
        S.finalize(rows, root)
    answer_audit(root, "confirm", lambda rid: "wrong_gold")
    out = S.finalize(rows, root)
    assert out["confirmed_rows"] == 12
    # incomplete reads block the final list unless explicitly allowed
    sc = S.jload(root / "reads" / "SCORE.json")
    sc["incomplete"] = ["t_src_yn_3"]
    S.jdump(sc, root / "reads" / "SCORE.json")
    with pytest.raises(SystemExit):
        S.finalize(rows, root)
    out = S.finalize(rows, root, allow_incomplete=True)
    assert S.jload(root / "REPLAY_UNSCREENED_A46.json")["drop_ids"] == ["t_src_yn_3"] and out["unscreened_rows"] == 1


def test_invalid_verdicts_are_problems_not_drops(root):
    rows, dbl = run_pipeline(root, None, None)
    S.adjudicate(rows, root, n_control=1)
    answer_audit(root, "adjudicate", lambda rid: "relabel_to_yes")
    with pytest.raises(SystemExit):
        S.confirm(rows, root)
    v, probs = S.load_verdicts(root, "adjudicate")
    assert v == {} and probs


def test_never_open_path_text_is_refused_not_read(root):
    rows = rows_of(root)
    rows[0]["state"] = "see /Users/aryamahadik/.claude/projects/x/y.txt for the lamp"
    info = S.build_reads(rows, root, bucket=60)
    assert info["n_refused"] >= 1 and info["n_rows"] == len(rows) - info["n_refused"]
    assert S.jload(root / "reads" / "REFUSED.json")[0]["row_id"] == rows[0]["id"]


def test_rebuild_refused_once_answers_exist(root):
    rows = rows_of(root)
    S.build_reads(rows, root, bucket=60)
    answer_reads(root)
    with pytest.raises(SystemExit):
        S.build_reads(rows, root, bucket=60)
    S.build_reads(rows, root, bucket=60, force=True)
