import gzip
import json

import pytest

import lr_common as lc
import lr_testlib as T
import taskmaster as K


def tm3(i, call):
    inp = ("<PR>get_movie_attribute<PRAN>rating.movie<PRAV>rated R<C><U>I wanna see a movie %d<A>where are you?"
           "<U>spring hills kansas<PN>find_theaters<PAN>location<PAV>spring hills kansas<PR>find_theaters<PRAN>name.theater"
           "<PRAV>AMC Holiday Theater<PRAV>Cinemark Downtown<A>there are 2 theaters near you.<U>funny one please %d") % (i, i)
    tgt = "[PN]find_movies[PAN]location[PAV]spring hills kansas" if call else "[A]Which one would you like?"
    return {"kind": "tm3", "input": inp, "target": tgt, "dlg_id": "dlg-%d" % (i // 2), "_src_line": "tm3:dlg-%d#%d" % (i // 2, i)}


NAMES = ["restaurant_reservation.name.restaurant", "restaurant_reservation.time.reservation", "pizza_ordering.type.topping",
         "movie_ticket.time.start", "uber_lyft.type.ride", "coffee_ordering.preference", "auto_repair.time.appt",
         "movie_ticket.name.movie", "coffee_ordering.name.drink", "pizza_ordering.name.pizza"]


def dialog(i):
    ut = [{"index": 0, "speaker": "USER", "text": "Hi, I want something for dinner %d" % i},
          {"index": 1, "speaker": "ASSISTANT", "text": "Sure, what would you like?"},
          {"index": 2, "speaker": "USER", "text": "A table at seven tonight at Luigi %d please" % i,
           "segments": [{"start_index": 8, "end_index": 12, "text": "seven", "annotations": [{"name": NAMES[(i + 1) % 10]}]},
                        {"start_index": 24, "end_index": 29, "text": "Luigi %d" % i, "annotations": [{"name": NAMES[i % 10]}]},
                        {"start_index": 30, "end_index": 33, "text": "two", "annotations": [{"name": NAMES[0]}, {"name": NAMES[1]}]}]}]
    return {"kind": "dialog", "dlg": {"conversation_id": "dlg-x%d" % i, "instruction_id": "r-1", "utterances": ut}, "_src_line": "tm1:dlg-x%d" % i}


def records(n=40):
    return [tm3(i, i % 2 == 0) for i in range(n)] + [dialog(i) for i in range(n)]


def test_rows_both_forms(monkeypatch):
    monkeypatch.setitem(K.RECAST_TABLE["caps"], K.F_ACT, 20)
    monkeypatch.setitem(K.RECAST_TABLE["caps"], K.F_SEG, 20)
    m = K.Mapper(T.pools_for(K.Mapper), seed=1)
    rows = m.map_records(records())
    T.check_rows(rows, m, min_rows=30)
    act = [r for r in rows if r["form"] == K.F_ACT]
    seg = [r for r in rows if r["form"] == K.F_SEG]
    assert act and seg
    assert sum(r["answer_text"] == "Yes" for r in act) == len(act) // 2          # balanced
    for r in act:
        assert "find_movies" not in r["context"]                                  # the target (next move) is never shown
        assert not r["context"].startswith("<PR>")                                # meta before <C> dropped
    for r in seg:
        assert r["context"].rstrip().endswith('"') and "Highlighted span:" in r["context"]
        assert r["answer_text"] in r["options"] and len(r["options"]) in (4, 8)


def test_render_tm3_input():
    lines = K.render_tm3_input(tm3(2, True)["input"])
    assert lines[0].startswith("Customer: I wanna see a movie 2") and lines[1] == "Assistant: where are you?"
    assert "[tool call: find_theaters(location=spring hills kansas)]" in lines
    assert "[tool result: find_theaters -> name.theater=AMC Holiday Theater, Cinemark Downtown]" in lines
    assert lines[-1].startswith("Customer: funny one please")


def test_two_names_span_skipped():
    items = K.seg_items(dialog(1))
    texts = [dialog(1)["dlg"]["utterances"][2]["segments"][it[2]]["text"] for it in items]
    assert "two" not in texts and len(items) == 2


def test_unusable_tm3_target_dropped_and_r4():
    m = K.Mapper(T.pools_for(K.Mapper), seed=1)
    bad = dict(tm3(0, True), target="[U]something")
    assert m.map_records([bad]) == []          # an unknown target prefix never becomes a row (counted in the selection step)
    assert m.build(bad, {}) == [] and m.drops.c["tm3_unusable_example"] == 1
    m2 = K.Mapper(T.pools_for(K.Mapper), seed=1)
    m2.independent_gold = lambda s, c: "?"
    assert m2.map_records(records(6)) == []


def test_reader_train_files_only(tmp_path):
    with gzip.open(tmp_path / "tm1_train.json.gz", "wt") as f:
        json.dump([dialog(1)["dlg"]], f)
    with gzip.open(tmp_path / "tm2_music.holdout10.json.gz", "wt") as f:
        json.dump([dialog(2)["dlg"]], f)
    with gzip.open(tmp_path / "tm3_train.tsv.gz", "wt") as f:
        r = tm3(1, True)
        f.write("\t".join([r["input"], r["target"], r["dlg_id"]]) + "\n")
    got = list(K.read_train(str(tmp_path)))
    assert [g["kind"] for g in got] == ["dialog", "tm3"] and got[0]["_src_line"].startswith("tm1:")


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(K.Mapper)
