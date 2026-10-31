import json

import pytest

import lr_common as lc
import lr_testlib as T
import snips_2017_06 as S

INTENTS = ["AddToPlaylist", "BookRestaurant", "GetWeather", "PlayMusic", "RateBook", "SearchCreativeWork", "SearchScreeningEvent"]


def records(n=20):
    out = []
    for i in range(n):
        it = INTENTS[i % 7]
        data = [{"text": "Please do the thing number %d with " % i}, {"text": "artist%d name" % i, "entity": "artist"},
                {"text": " in the "}, {"text": "city%d" % i, "entity": "city"}, {"text": " today"}]
        out.append({"intent": it, "data": data, "_src_line": "train_%s_full.json#%d" % (it, i)})
    return out


def test_rows_both_forms():
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    rows = m.map_records(records())
    T.check_rows(rows, m, expect_kind=("choice",), min_rows=20)
    it = [r for r in rows if r["form"] == S.F_INTENT]
    sl = [r for r in rows if r["form"] == S.F_SLOT]
    assert it and sl
    assert all(r["k"] == 7 for r in it)                                  # <= 8 labels: all shown (LR-B1)
    assert all(3 <= r["k"] <= 4 for r in sl)
    for r in sl:
        assert r["answer_text"] in r["context"]                          # gold span is inside the utterance
        assert all(o in r["context"] or o.strip() in r["context"] for o in r["options"])   # distractors from the SAME utterance
        assert r["extra"]["entity"] in ("artist", "city")


def test_flatten_offsets():
    text, spans = S.flatten(records(1)[0]["data"])
    assert [text[a:b] for _, a, b in spans] == ["artist0 name", "city0"]


def test_ambiguous_slot_and_bad_encoding_dropped():
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    twice = {"intent": "GetWeather", "_src_line": "x#1",
             "data": [{"text": "a "}, {"text": "foo", "entity": "city"}, {"text": " b "}, {"text": "bar", "entity": "city"}]}
    bad = {"intent": "GetWeather", "_src_line": "x#2", "data": [{"text": "caf� please"}]}
    rows = m.map_records([twice, bad] + records(7))
    assert not [r for r in rows if r["source_row_id"] in ("snips:x#1", "snips:x#2") and r["form"] == S.F_SLOT]
    assert m.drops.c.get("empty_or_bad_encoding", 0) >= 1


def test_duplicates_dropped_and_r4():
    m = S.Mapper(T.pools_for(S.Mapper), seed=1)
    r = records(3)
    rows = m.map_records(r + [dict(r[0], _src_line="dup#1")])
    assert m.drops.c["duplicate_item"] == 1
    m2 = S.Mapper(T.pools_for(S.Mapper), seed=1)
    m2.independent_gold = lambda s, c: "zzz"
    assert m2.map_records(records(4)) == []


def test_reader_train_files_only_and_replacement_char(tmp_path):
    (tmp_path / "train_GetWeather.json").write_bytes(json.dumps({"GetWeather": [{"data": [{"text": "weather in "}, {"text": "Paris", "entity": "city"}]}]}).encode())
    (tmp_path / "validate_GetWeather.json").write_text(json.dumps({"GetWeather": [{"data": [{"text": "HELD OUT"}]}]}))
    (tmp_path / "train_PlayMusic_full.json").write_bytes(b'{"PlayMusic": [{"data": [{"text": "play caf\xed"}]}]}')
    got = list(S.read_train(str(tmp_path)))
    assert len(got) == 2 and all("HELD OUT" not in json.dumps(g) for g in got)


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(S.Mapper)
