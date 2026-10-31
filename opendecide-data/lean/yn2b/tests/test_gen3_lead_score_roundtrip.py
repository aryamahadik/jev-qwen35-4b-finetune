"""F5 rows as the trainer and JevBench read them: mv_core.assemble -> golden rows -> decoder_io's cygnet prompt
(layout schema_branch_mark) -> every option survives, yes/no rows are Yes/No letter choices with the card printed as
Definitions, score rows list the level texts in ascending order with no card, JB rows have no card. Then
train_decoder.check_rows(kd=0.5) and make_units (no merges: every relation is inside one call_id unit).
decoder_io / prism_x / train_decoder are imported read-only (prompt building only; no model is loaded)."""
from __future__ import annotations

import re

import pytest

from f5_helpers import g, mv, small_build

decoder_io = pytest.importorskip("decoder_io")
prism_x = pytest.importorskip("prism_x")


@pytest.fixture(scope="module")
def golden():
    fb, _ = small_build()
    return mv.assemble(fb.rows, fb.rels, lambda r: fb.defs.get(r["meta"]["defs"]))


@pytest.fixture(autouse=True)
def _layout():
    old = (decoder_io.STYLE, decoder_io.LAYOUT)
    decoder_io.STYLE, decoder_io.LAYOUT = "cygnet", "schema_branch_mark"
    yield
    decoder_io.STYLE, decoder_io.LAYOUT = old


def test_prompt_round_trip(golden):
    rows, _ = golden
    assert len(rows) > 250
    for row in rows:
        r = decoder_io.as_letter_row(row)
        parts = decoder_io.cygnet_parts(r, None)
        msg = decoder_io.cygnet_msg(r, None)
        assert "\n".join(s for _, s in parts) == msg == decoder_io.user_msg(row)
        opts = r["options"]
        opt_lines = [s for t, s in parts if t == "opt"]
        assert len(opt_lines) == len(opts)
        defs = decoder_io.card_defs(row.get("card"))
        for i, o in enumerate(opts):
            want = f"{decoder_io.label(i)}. {o}: {defs[o]}" if o in defs else f"{decoder_io.label(i)}. {o}"
            assert opt_lines[i] == want
        data = [s for t, s in parts if t == "data"]
        assert data == [f"{decoder_io.UNTRUSTED[0]}\n{row['state'].rstrip()}\n{decoder_io.UNTRUSTED[1]}"]
        m = row["meta"]
        if m["qkind"] == "yn":
            assert row["qtype"] == "noul" and row["options"] is None and type(row["gold"]) is int
            assert r["options"] == ["Yes", "No"]
            if row["card"]:
                assert msg.startswith("Definitions:\n" + row["card"] + "\n")
                assert {k.lower() for k in decoder_io.card_defs(row["card"])} == {"yes", "no"}
        elif m["qkind"] == "score":
            assert row["qtype"] == "choice" and row["card"] is None and m["levels"] == len(row["options"])
            assert not any(re.match(r"^\d+\s*:", o) for o in row["options"])
            assert row["gold"] in row["options"]
        elif m["qkind"] == "jb":
            assert row["qtype"] == "choice" and row["card"] is None and len(row["options"]) == 2


def test_prism_x_data_span(golden):
    rows, _ = golden
    for row in rows[:400]:
        r = decoder_io.as_letter_row(row)
        msg = decoder_io.cygnet_msg(r, None)
        text = "<|system|>sys\n<|user|>\n" + msg + "\n<|assistant|>\n"
        sp = prism_x.row_char_spans(row, None, text)
        s, e = sp["data"]
        assert text[s:e] == f"{decoder_io.UNTRUSTED[0]}\n{row['state'].rstrip()}\n{decoder_io.UNTRUSTED[1]}"


def test_golden_fields_and_trainer_checks(golden):
    rows, rels = golden
    for r in rows:
        assert r["id"].startswith(f"r_yn2b_{g.KEY}_") and r["source"] == f"gd_{g.KEY}" and r["track"] == "GD"
        assert r["group_id"] == f"g:yn2b:{g.KEY}:{r['meta']['latent_id']}" and r["call_id"] == mv.cid(r["group_id"])
        assert "teacher" not in r["meta"]
    td = pytest.importorskip("train_decoder")
    td.check_rows(rows, kd=0.5)
    units, merged = td.make_units(rows, rels)
    assert merged == 0 and max(len(u) for u in units) <= mv.UNIT_MAX_ROWS
    assert {x["type"] for x in rels} == {"equiv", "inv"}  # F5 has no complement ladders (SPEC 4.2: F4 quads only)
