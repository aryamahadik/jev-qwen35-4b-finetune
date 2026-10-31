"""Round trip: mv_core rows -> golden rows -> the exact prompt decoder_io builds (layout schema_branch_mark, cygnet
style) -> every card line and every option survives; yes/no rows have options null and gold 0/1; score rows show the
level texts in ascending order. Also: PRISM-X spans, train_decoder.check_rows, writing + manifest + read-back.

decoder_io / prism_x / train_decoder are imported read-only (prompt building only; no model is loaded).
Run: PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider yn2b/tests
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
LEAN = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(LEAN))
import toy_family as toy  # noqa: E402
import mv_core as mv  # noqa: E402

decoder_io = pytest.importorskip("decoder_io")
prism_x = pytest.importorskip("prism_x")


@pytest.fixture(scope="module")
def built(tmp_path_factory):
    d = tmp_path_factory.mktemp("rt")
    fb = mv.FamilyBuilder(toy.KEY, generator_file=toy.__file__, raw_dir=d / "raw", defs_dir=d / "defs",
                          manifest=d / "MANIFEST_yn2b.jsonl", tier_shares={"easy": 0.3, "standard": 0.4, "hard": 0.3})
    toy.build(fb, "train", 240)
    toy.build(fb, "dev_iid", 30)
    toy.build(fb, "dev_holdout", 30)
    rows, rels = mv.assemble(fb.rows, fb.rels, lambda r: fb.defs.get(r["meta"]["defs"]))
    return fb, rows, rels, d


@pytest.fixture(autouse=True)
def _layout():
    old = (decoder_io.STYLE, decoder_io.LAYOUT)
    decoder_io.STYLE, decoder_io.LAYOUT = "cygnet", "schema_branch_mark"
    yield
    decoder_io.STYLE, decoder_io.LAYOUT = old


def test_markers_match_decoder_io():
    assert tuple(mv.MARKERS) == tuple(decoder_io.UNTRUSTED)
    assert mv.JB_FALLBACK == ("yes, this holds", "no, this does not hold")


def test_card_defs_identical_to_decoder_io(built):
    _, rows, _, _ = built
    probes = [r.get("card") for r in rows] + [
        None, "", "- a: b", "- a: b: c", "-a: b", "- a:b", "- Yes: x\n- No: y", "junk\n- k: v\n", "- : v"]
    for c in probes:
        assert mv.card_defs(c) == decoder_io.card_defs(c)


def test_every_view_type_is_present(built):
    _, rows, rels, _ = built
    views = {r["meta"]["view"] for r in rows}
    qk = {r["meta"]["qkind"] for r in rows}
    assert {"base", "contrast", "ladder", "format", "mirror", "jb", "attack"} <= views
    assert {"yn", "choice", "score", "jb"} <= qk
    assert {x["type"] for x in rels} == {"complement", "equiv", "inv"}
    assert {r["meta"]["card_style"] for r in rows if r["qtype"] == "noul"} == {"lower", "upper", "none"}
    assert any(r["meta"].get("plant_spoof") for r in rows)


def _check_prompt(row, perm=None):
    r = decoder_io.as_letter_row(row)
    msg = decoder_io.cygnet_msg(r, perm)
    parts = decoder_io.cygnet_parts(r, perm)
    assert "\n".join(s for _, s in parts) == msg
    if perm is None:
        assert decoder_io.user_msg(row) == msg
    opts = r["options"] if perm is None else [r["options"][i] for i in perm]
    opt_lines = [s for t, s in parts if t == "opt"]
    assert len(opt_lines) == len(opts)
    defs = decoder_io.card_defs(row.get("card"))
    for i, o in enumerate(opts):  # every option survives, with its definition when it has one
        want = f"{decoder_io.label(i)}. {o}: {defs[o]}" if o in defs else f"{decoder_io.label(i)}. {o}"
        assert opt_lines[i] == want
    card = row.get("card")
    if row["qtype"] == "noul":
        assert row["options"] is None and row["gold"] in (0, 1) and type(row["gold"]) is int
        assert r["options"] == ["Yes", "No"] and r["gold"] == ("Yes" if row["gold"] == 1 else "No")
        if card:  # the whole card is printed as trusted definitions
            assert ("ins", card) in parts
            assert msg.startswith("Definitions:\n" + card + "\n")
            for line in card.split("\n"):
                assert line in msg
        else:
            assert not msg.startswith("Definitions:")
    else:
        assert not any(t == "ins" and s == card for t, s in parts if card)
        if card:  # a choice card is shown ONLY through option lines: every line must key an option
            for line in card.split("\n"):
                k, v = line[2:].split(": ", 1)
                assert k in opts and f". {k}: {v}" in "\n".join(opt_lines), line
        assert row["gold"] in row["options"]
    data = [s for t, s in parts if t == "data"]
    assert data == [f"{decoder_io.UNTRUSTED[0]}\n{row['state'].rstrip()}\n{decoder_io.UNTRUSTED[1]}"]
    assert row["instructions"].rstrip() in [s for t, s in parts if t == "ins"]
    return msg, parts


def test_prompt_round_trip_every_row(built):
    _, rows, _, _ = built
    assert len(rows) > 800
    for row in rows:
        _check_prompt(row)


def test_prompt_round_trip_permuted(built):
    _, rows, _, _ = built
    perms = decoder_io.view_perms(rows, seed=7)
    for row, p in zip(rows, perms):
        _check_prompt(row, p)


def test_yes_no_and_score_formats(built):
    _, rows, _, _ = built
    n_score = 0
    for row in rows:
        m = row["meta"]
        if m["qkind"] == "yn":
            assert row["qtype"] == "noul" and row["options"] is None and row["gold"] in (0, 1)
            if m["card_style"] == "lower":
                assert row["card"].split("\n")[-2].startswith("- yes: ") and row["card"].split("\n")[-1].startswith("- no: ")
            elif m["card_style"] == "upper":
                assert row["card"].split("\n")[-2].startswith("- Yes: ") and row["card"].split("\n")[-1].startswith("- No: ")
            else:
                assert row["card"] is None
        elif m["qkind"] == "score":
            n_score += 1
            assert row["qtype"] == "choice" and row["card"] is None and m["levels"] == len(row["options"])
            assert not any(re.match(r"^\d+\s*:", o) for o in row["options"])
            L = int(re.fullmatch(r"over (\d+) g", row["options"][-1]).group(1))
            assert row["options"] == toy.score_levels({"limit": L})  # ascending level texts, as given
            assert row["gold"] in row["options"]
        elif m["qkind"] == "jb":
            assert row["qtype"] == "choice" and row["card"] is None and len(row["options"]) == 2
            assert tuple(row["options"]) in ((toy.JB_YES, toy.JB_NO), mv.JB_FALLBACK)
        else:
            assert row["qtype"] == "choice"
    assert n_score > 20


def test_prism_x_spans(built):
    _, rows, _, _ = built
    for row in rows:
        msg, parts = _check_prompt(row)
        text = "<|system|>sys\n<|user|>\n" + msg + "\n<|assistant|>\n"
        sp = prism_x.row_char_spans(row, None, text)
        r = decoder_io.as_letter_row(row)
        assert len(sp["opt"]) == len(r["options"])
        s, e = sp["data"]
        assert text[s:e] == f"{decoder_io.UNTRUSTED[0]}\n{row['state'].rstrip()}\n{decoder_io.UNTRUSTED[1]}"
        if row["meta"].get("plant_spoof"):  # a spoofed END marker stays inside the data span (roles are positional)
            k = text.find(decoder_io.UNTRUSTED[1], s + len(decoder_io.UNTRUSTED[0]))
            assert s < k < e - len(decoder_io.UNTRUSTED[1])


def test_no_markers_outside_spoof_rows(built):
    _, rows, _, _ = built
    for row in rows:
        texts = [row["instructions"], row.get("card") or ""] + list(row["options"] or [])
        assert not any(m in t for t in texts for m in mv.MARKERS)
        if not row["meta"].get("plant_spoof"):
            assert not any(m in row["state"] for m in mv.MARKERS)


def test_train_decoder_check_rows(built):
    td = pytest.importorskip("train_decoder")
    _, rows, rels, _ = built
    td.check_rows(rows, kd=0.5)
    assert not any("teacher" in r["meta"] for r in rows)
    units, merged = td.make_units(rows, rels)
    assert merged == 0  # every related pair already shares its call_id
    assert max(len(u) for u in units) <= mv.UNIT_MAX_ROWS


def test_golden_fields(built):
    _, rows, rels, _ = built
    for r in rows:
        assert r["id"].startswith(f"r_yn2b_{toy.KEY}_")
        assert r["group_id"] == f"g:yn2b:{toy.KEY}:{r['meta']['latent_id']}"
        assert r["call_id"] == mv.cid(r["group_id"]) and r["track"] == "GD" and r["source"] == f"gd_{toy.KEY}"
        assert r["split"] == {None: "train", "iid": "yn2b_dev", "holdout": "yn2b_dev"}[r["meta"]["dev_kind"]]
        assert r["role"] in mv.ROLES
    by = {r["id"]: r for r in rows}
    for x in rels:
        assert x["track"] == by[x["a"]]["split"]
    twins = [r for r in rows if r["meta"]["twin_of"]]
    assert twins and all(r["meta"]["twin_of"] in by and by[r["meta"]["twin_of"]]["gold"] != r["gold"] for r in twins)


def test_write_manifest_and_read_back(built, tmp_path):
    fb, rows, rels, d = built
    out = fb.write()
    rp, lp = mv.raw_paths(toy.KEY, "train", d / "raw")
    dp, _ = mv.raw_paths(toy.KEY, "dev", d / "raw")
    assert rp.exists() and lp.exists() and dp.exists()
    man = [json.loads(x) for x in open(d / "MANIFEST_yn2b.jsonl")]
    by = {m["path"]: m for m in man}
    for p in (rp, lp, dp):
        m = by[str(p.resolve())]
        assert m["sha256"] == mv.sha256_file(p) == out[str(p)]
        assert m["rows"] == sum(1 for _ in open(p))
    assert any(m["part"] == "defs" for m in man)
    raw_tr, rel_tr = mv.read_raw(toy.KEY, "train", d / "raw")
    raw_dv, rel_dv = mv.read_raw(toy.KEY, "dev", d / "raw")
    assert raw_tr + raw_dv == fb.rows
    back, back_rels = mv.assemble(raw_tr + raw_dv, rel_tr + rel_dv,
                                  lambda r: mv.load_defs(r["key"], r["meta"]["defs"], d / "defs"))
    assert back == rows and sorted(map(json.dumps, back_rels)) == sorted(map(json.dumps, rels))
    for r in raw_tr:  # fixed raw meta key set (SPEC 4.10 + check keys)
        assert tuple(r["meta"]) == mv.RAW_META_KEYS
        assert set(r) == {"key", "rid", "state", "instructions", "options", "gold", "soft", "meta"}
        assert r["meta"]["licence"] == mv.LICENCE and r["meta"]["split"] == "train" and r["soft"] is None
        if r["meta"]["qkind"] == "yn":
            assert r["options"] == ["yes", "no"] and r["gold"] in ("yes", "no")
    fb2 = mv.FamilyBuilder(toy.KEY, generator_file=toy.__file__, raw_dir=d / "raw", defs_dir=d / "defs",
                           manifest=d / "MANIFEST_yn2b.jsonl")
    fb2.defs = {q: {"yes": "changed", "no": "changed"} for q in fb.defs}
    fb2.rows = fb.rows
    with pytest.raises(RuntimeError):  # content-addressed defs never silently change
        fb2.write(parts=())


def test_labels_agree_with_independent_decide2(built):
    fb, _, _, _ = built
    rep = mv.verify_labels(fb.rows, toy.decide2_row)
    assert rep["ok"] and rep["disagree"] == 0 and rep["rows"] == len(fb.rows)
