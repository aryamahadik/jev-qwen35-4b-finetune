import zipfile

import pytest

import lr_common as lc
import lr_testlib as T
import logchunks as L


def make_log(i, n=120):
    lines = ["$ step %d line %d building module %d" % (i, j, j * 3 + i) for j in range(n)]
    lines[40] = "npm ERR! missing script: build-%d" % i
    lines[41] = "npm ERR! A complete log of this run can be found in: /tmp/npm-%d.log" % i
    lines[42] = "The command \"npm run build-%d\" exited with 1." % i
    lines[70] = "\x1b[31mwarning: deprecated api %d\x1b[0m" % i
    return "\r\n".join(lines)


def records(n=20):
    out = []
    for i in range(n):
        chunk = "m ERR! missing script: build-%d\nnpm ERR! A complete log of this run can be found in: /tmp/npm-%d.log\nThe command \"npm run build-%d\" exited with 1." % (i, i, i)
        out.append({"log_id": "JavaScript/own@repo%d/failed/%d.log" % (i % 3, 1000 + i), "language": "JavaScript",
                    "repo": "own@repo%d" % (i % 3), "keywords": ["ERR", "warning"], "category": "0", "chunk": chunk,
                    "log_text": make_log(i), "_src_line": "JavaScript/own@repo%d/failed/%d.log" % (i % 3, 1000 + i)})
    return out


def test_rows():
    m = L.Mapper(T.pools_for(L.Mapper), seed=1)
    rows = m.map_records(records())
    T.check_rows(rows, m, expect_kind=("choice",), min_rows=20)
    assert {r["k"] for r in rows} <= {4, 8}
    for r in rows:
        assert "\x1b" not in r["context"]
        # the gold segment holds the labelled lines; the options are exactly the displayed segment names
        assert r["options"].count(r["answer_text"]) == 1
        seg = r["context"].split("[Segment %s]" % r["answer_text"].split()[1])[1]
        assert "missing script: build-" in seg
    rep = T.check_set_report(rows)
    assert rep["R6_pass"] and rep["R5_position_pass"]


def test_locate_chunk_tolerates_trimmed_ends_and_ansi():
    lines = ["a", "\x1b[31m[error]\x1b[0m /src/x.scala:10:8: object missing", "  at foo", "[error] total time", "z"]
    chunk = "error] /src/x.scala:10:8: object missing\n  at foo\n[error] total"
    assert L.locate_chunk(lines, chunk) == (1, 3)
    assert L.locate_chunk(lines, "") is None and L.locate_chunk(lines, "short") is None
    assert L.locate_chunk(lines, "not present anywhere in this log") is None


def test_segments_random_order_and_gold_not_always_first():
    m = L.Mapper(T.pools_for(L.Mapper), seed=7)
    rows = m.map_records(records(20))
    golds = {r["answer_text"] for r in rows}
    assert len(golds) > 1
    firsts = sum(r["context"].split("\n\n")[0].count("missing script") for r in rows)
    assert firsts < len(rows)               # gold is not always displayed first


def test_unlocatable_and_oversize_gold_dropped():
    m = L.Mapper(T.pools_for(L.Mapper), seed=1)
    bad = dict(records(1)[0], chunk="this chunk text is not in the log at all")
    big_log = "\n".join("same filler line number %d here" % j for j in range(300))
    big = dict(records(1)[0], log_text=big_log, chunk="\n".join("same filler line number %d here" % j for j in range(10, 90)),
               _src_line="x/big")
    assert m.map_records([bad, big]) == []
    assert m.drops.c["chunk_not_locatable"] == 1 and m.drops.c["gold_chunk_over_60_lines"] == 1


def test_r4_mismatch_dropped():
    m = L.Mapper(T.pools_for(L.Mapper), seed=1)
    m.independent_gold = lambda s, c: "Segment 99"
    assert m.map_records(records(3)) == [] and m.drops.c["R4_gold_mismatch"] == 3


def test_reader_only_train_zip(tmp_path):
    xml = ('<?xml version="1.0"?><Examples><Example><Log>Go/o@r/failed/1.log</Log><Keywords>err</Keywords><Category>0</Category>'
           '<Chunk>boom happened here</Chunk></Example></Examples>')
    with zipfile.ZipFile(tmp_path / "logchunks_train.zip", "w") as z:
        z.writestr("LogChunks/build-failure-reason/Go/o@r.xml", xml)
        z.writestr("LogChunks/logs/Go/o@r/failed/1.log", "x\nboom happened here\ny")
    got = list(L.read_train(str(tmp_path)))
    assert len(got) == 1 and got[0]["repo"] == "o@r" and got[0]["chunk"] == "boom happened here"
    with pytest.raises(AssertionError):
        list(L.read_train("/x/bench/c21_eval_quarantine/lr_targets/logchunks"))


def test_refuses_non_dry_run():
    T.check_dry_run_refusal(L.Mapper)
