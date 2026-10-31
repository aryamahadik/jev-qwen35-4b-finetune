import csv

import lr_common as lc
import lr_testlib as T
import ethics_mturk as E


def records(n=20):
    out = []
    for i in range(n):
        lab = str(i % 2)
        out.append({"form": E.F_JUS, "row": {"label": lab, "scenario": "I deserve thing %d because of reason %d." % (i, i)}, "_src_line": "ethics:justice#%d" % i})
        out.append({"form": E.F_DEO, "row": {"label": lab, "scenario": "Aren't you supposed to do task %d?" % i, "excuse": "No because of excuse %d." % i}, "_src_line": "ethics:deontology#%d" % i})
        out.append({"form": E.F_VIR, "row": {"label": lab, "scenario": "Jill did act number %d. [SEP] trait%d" % (i, i % 5)}, "_src_line": "ethics:virtue#%d" % i})
        out.append({"form": E.F_UTL, "row": {"baseline": "I had a great day number %d." % i, "less_pleasant": "I had a bad day number %d." % i}, "_src_line": "ethics:utilitarianism#%d" % i})
        out.append({"form": E.F_COM, "row": {"label": lab, "input": "I did action number %d to someone." % i, "is_short": "True"}, "_src_line": "ethics:commonsense#%d" % i})
    return out


def test_rows_all_five_forms_and_balance():
    m = E.Mapper(T.pools_for(E.Mapper), seed=1)
    rows = m.map_records(records(20))
    T.check_rows(rows, m, min_rows=50)
    forms = {r["form"] for r in rows}
    assert forms == set(E.FORMS)
    for f in (E.F_JUS, E.F_DEO, E.F_VIR, E.F_COM):
        rr = [r for r in rows if r["form"] == f]
        assert abs(sum(r["answer_text"] == "Yes" for r in rr) - len(rr) / 2) <= 1
    utl = [r for r in rows if r["form"] == E.F_UTL]
    assert all(r["k"] == 2 and r["answer_text"].startswith("I had a great day") for r in utl)


def test_virtue_slot_and_label_mapping():
    pools = lc.WordingPools({E.F_VIR: ["Does the person show {trait}? [v%02d]" % i for i in range(60)]}, placeholder=True)
    pools.pools.update({f: ["%s [v%02d]" % (b, i) for i in range(60)] for f, b in E.FORMS.items() if f != E.F_VIR})
    m = E.Mapper(pools, seed=1)
    rows = m.map_records(records(10))
    v = [r for r in rows if r["form"] == E.F_VIR]
    assert v and all(any(("trait%d" % t) in r["stem"] for t in range(5)) for r in v)
    for r in rows:
        if r["form"] != E.F_UTL:
            i = int(r["source_row_id"].split("#")[1])
            assert r["answer_text"] == ("Yes" if i % 2 else "No")


def test_virtue_one_row_per_scenario():
    m = E.Mapper(T.pools_for(E.Mapper), seed=1)
    recs = [{"form": E.F_VIR, "row": {"label": str(t % 2), "scenario": "Same scenario text. [SEP] trait%d" % t}, "_src_line": "ethics:virtue#%d" % t} for t in range(5)]
    assert len(m.map_records(recs)) == 1


def test_identical_pair_and_empty_dropped_r4():
    m = E.Mapper(T.pools_for(E.Mapper), seed=1)
    recs = [{"form": E.F_UTL, "row": {"baseline": "same", "less_pleasant": "same"}, "_src_line": "ethics:utilitarianism#1"},
            {"form": E.F_JUS, "row": {"label": "1", "scenario": "  "}, "_src_line": "ethics:justice#1"}]
    assert m.map_records(recs) == [] and m.drops.c["empty_or_identical_pair"] == 1 and m.drops.c["empty_text"] == 1
    m.independent_gold = lambda s, c: "?"
    assert m.map_records(records(2)) == []


def test_reader_train_files_only(tmp_path):
    for sub, hdr in (("justice", "label,scenario"), ("commonsense", "label,input,is_short,edited")):
        (tmp_path / sub).mkdir()
    (tmp_path / "justice" / "train.csv").write_text("label,scenario\n1,I deserve it.\n")
    (tmp_path / "justice" / "test.csv").write_text("label,scenario\n1,HELD OUT.\n")
    (tmp_path / "commonsense" / "train.short.csv").write_text("label,input,is_short,edited\n0,Short one.,True,False\n")
    got = list(E.read_train(str(tmp_path)))
    assert sorted(g["form"] for g in got) == sorted([E.F_JUS, E.F_COM]) and all("HELD" not in str(g) for g in got)


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(E.Mapper)
