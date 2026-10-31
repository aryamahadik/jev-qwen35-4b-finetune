"""CPU tests for modal_label_rev.py and merge_rev.py (no model weights, no network, nothing launched).

  cd lean && ../.venv/bin/python -m pytest -q extra/test_label_rev.py
  cd lean && ../.venv/bin/python extra/test_label_rev.py --all-views   # also: stored view == view_perms on all 20 shards
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest
import torch

HERE = Path(__file__).resolve().parent
LEAN = HERE.parent
for p in (str(LEAN), str(HERE)):
    if p not in sys.path:
        sys.path.insert(0, p)
import decoder_io  # noqa: E402
import merge_rev  # noqa: E402
import modal_label_rev as mlr  # noqa: E402
import shard_golden as sg  # noqa: E402

SHARDS = LEAN / "data/v14_label_shards"
ORIG = SHARDS / "labels_q35_4b_pxE"


def test_image_pins_equal_modal_od():
    import modal_od
    assert mlr.PINNED35 == modal_od.PINNED35
    assert "3.12.10" in (LEAN / "modal_od.py").read_text()
    src = (LEAN / "modal_od.py").read_text()
    for k, v in mlr.ENV35.items():
        assert f'"{k}": "{v}"' in src
    assert mlr.APP_NAME != modal_od.app.name
    assert "q35_4b_main500k" not in mlr.OUT and mlr.OUT.startswith("/vol/label_shards/labels_q35_4b_pxE_rev")


def test_reverse_view():
    assert mlr.reverse_views([[1, 3, 2, 0], [0, 1]]) == [[0, 2, 3, 1], [1, 0]]
    v = [2, 0, 1]
    assert mlr.reverse_views([v]) == [[1, 0, 2]] and v == [2, 0, 1]  # input not mutated


def test_perm_semantics_display_and_keys():
    """perm[k] = ORIGINAL index shown at display position k; probs come back keyed by option text."""
    row = {"id": "x", "qtype": "choice", "options": ["o0", "o1", "o2", "o3"], "state": "s", "instructions": "q?",
           "gold": "o2"}
    view = [1, 3, 2, 0]
    rev = mlr.reverse_views([view])[0]  # [0, 2, 3, 1]
    old = (decoder_io.STYLE, decoder_io.LAYOUT)
    try:
        decoder_io.STYLE, decoder_io.LAYOUT = "cygnet", "schema_branch_mark"
        msg = decoder_io.cygnet_msg(row, view)
        assert "A. o1" in msg and "D. o0" in msg
        msg2 = decoder_io.cygnet_msg(row, rev)
        assert "A. o0" in msg2 and "D. o1" in msg2
        logits = torch.tensor([5.0, 0.0, 0.0, 0.0])  # the model always picks the letter A
        p1 = decoder_io._in_order(row, decoder_io.to_probs(row, logits, view))
        p2 = decoder_io._in_order(row, decoder_io.to_probs(row, logits, rev))
        assert max(p1, key=p1.get) == "o1" and max(p2, key=p2.get) == "o0"
        assert list(p1) == row["options"]
    finally:
        decoder_io.STYLE, decoder_io.LAYOUT = old


def test_predict_tta_uses_the_same_reversal():
    """decoder_io.predict's own TTA reverses a view with view[::-1]: the rev job reproduces that second read."""
    src = (LEAN / "decoder_io.py").read_text()
    assert 'rev = [view(i, len(rows[i]["options"]))[::-1] for _, i in ch]' in src


def _stored_views_match(shard_idx):
    sp = SHARDS / sg.shard_name(shard_idx)
    rs = mlr.choice_rows(sg.read_jsonl(sp))
    views = mlr.seeded_views(rs)
    return mlr.check_stored_views(rs, views, sg.label_paths(ORIG, sp)[0])


@pytest.mark.skipif(not (ORIG / "shard_007.jsonl").exists(), reason="local labels missing")
def test_stored_views_are_view_perms_shard7():
    assert _stored_views_match(7) > 500


def fake_predict(rows, perms):
    """Position-biased fake model through the real to_probs/_in_order path: favours display position 0."""
    out = []
    for r, p in zip(rows, perms):
        n = len(r["options"])
        lg = torch.tensor([2.0] + [0.0] * (n - 1))
        out.append(decoder_io._in_order(r, decoder_io.to_probs(r, lg, p)))
    return out


@pytest.mark.skipif(not (ORIG / "shard_007.jsonl").exists(), reason="local labels missing")
def test_end_to_end_rev_then_merge(tmp_path):
    sd = tmp_path / "shards"
    sd.mkdir()
    shutil.copy(SHARDS / "shard_007.jsonl", sd / "shard_007.jsonl")
    od = tmp_path / "orig"
    od.mkdir()
    for f in ("shard_007.jsonl", "shard_007.meta.json"):
        shutil.copy(ORIG / f, od / f)
    out = tmp_path / "rev"
    shas = mlr.local_shas()
    commits = []
    s = mlr.label_rev_shards([7], sd, od, out, fake_predict, shas, lambda: commits.append(1))
    assert s[0]["rows"] == 572 and s[0]["views_checked"] == 572 and commits == [1]
    recs = sg.read_jsonl(out / "shard_007.jsonl")
    orig = {x["id"]: x for x in sg.read_jsonl(od / "shard_007.jsonl")}
    rows = {r["id"]: r for r in sg.read_jsonl(sd / "shard_007.jsonl")}
    for x in recs:
        assert x["view"] == orig[x["id"]]["view"][::-1]
        top = max(x["probs"], key=x["probs"].get)
        assert top == rows[x["id"]]["options"][x["view"][0]]  # display position 0 of the REVERSED view
    # resumable: a second call skips; other settings refuse
    assert mlr.label_rev_shards([7], sd, od, out, fake_predict, shas)[0]["skipped"] == "done"
    with pytest.raises(SystemExit):
        mlr.label_rev_shards([7], sd, od, out, fake_predict, shas, settings={**mlr.SETTINGS, "perm_seed": 1})
    # wrong shard set refuses
    with pytest.raises(RuntimeError):
        mlr.label_rev_shards([7], sd, od, tmp_path / "rev2", fake_predict, {7: "0" * 64})
    # deadline: a shard that cannot finish is not started
    assert mlr.label_rev_shards([7], sd, od, tmp_path / "rev3", fake_predict, shas, stop_at_unix=1.0)[0]["skipped"] \
        == "deadline"
    # merge
    m = tmp_path / "m"
    rc = merge_rev.main(["--orig", str(od), "--rev", str(out), "--shards-dir", str(sd), "--out", str(m)])
    assert rc == 0
    merged = sg.load_labels(m, sd)  # drop-in for build_2b_kd (every row, meta vouches)
    assert len(merged) == 21102
    for i, x in orig.items():
        r = rows[i]
        if r["qtype"] != "choice":
            assert merged[i] == x["probs"]
        else:
            rv = {y["id"]: y for y in recs}[i]["probs"]
            assert all(abs(merged[i][o] - (x["probs"][o] + rv[o]) / 2) < 1e-12 for o in r["options"])
            assert abs(sum(merged[i].values()) - 1) < 1e-4
    # a missing rev shard -> exit 2, nothing written for it
    assert merge_rev.main(["--orig", str(od), "--rev", str(tmp_path / "none"), "--shards-dir", str(sd), "--out",
                           str(tmp_path / "m2")]) == 2


def test_parse_groups():
    assert mlr.parse_groups("0,1;2,3;4,5;6-19") == [[0, 1], [2, 3], [4, 5], list(range(6, 20))]
    with pytest.raises(SystemExit):
        mlr.parse_groups("0-3;3")


if __name__ == "__main__" and "--all-views" in sys.argv:
    tot = 0
    for i in range(20):
        n = _stored_views_match(i)
        tot += n
        print(i, n, flush=True)
    print("all stored choice views == view_perms:", tot)
