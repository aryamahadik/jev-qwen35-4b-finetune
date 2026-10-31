"""fastcore.readout on CPU: API v1 -> decoder_io rows (prompt identity on the dev splits), token caps, request errors,
and the 2view combine == decoder_io.predict(tta_choice=True) on a tiny random Qwen3.5 with the C1 tokenizer.

  cd ~/Documents/jev/opendecide-data/lean && ../.venv/bin/python -m pytest hosting/tests/test_fastcore_readout.py -q
No GPU, no network, no Modal; reads only the 9 gate dev splits and the local C1 tokenizer backup.
"""
import random
import sys
from pathlib import Path

import pytest
import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastcore import readout as R  # noqa: E402
from fastcore import testing as T  # noqa: E402

dio = R.dio


@pytest.fixture(scope="module")
def tok():
    return T.c1_tokenizer()


@pytest.fixture(scope="module")
def ro(tok):
    return T.readout()


@pytest.fixture(scope="module")
def rows():
    return T.dev_rows()


def _sample(rows, seed=0, per_split=70):
    rng = random.Random(seed)
    by = {}
    for r in rows:
        by.setdefault(r["_split"], []).append(r)
    out = []
    for sp in T.SPLITS:
        out += rng.sample(by[sp], min(per_split, len(by[sp])))
    wide = [r for r in rows if len(r["options"] or []) > 26]
    carded_noul = [r for r in rows if r["qtype"] == "noul" and r.get("card")]
    out += wide[:40] + rng.sample(carded_noul, 40)
    seen, uniq = set(), []
    for r in out:
        if r["id"] not in seen:
            seen.add(r["id"])
            uniq.append(r)
    return uniq


def test_layout_is_c1s(tok, ro):
    assert (dio.LAYOUT, dio.STYLE) == ("schema_branch_mark", "cygnet")
    assert R.max_options() == 255 and len(dio.WIDE) == 255


def test_prompt_identity_all_dev_rows(ro, rows):
    """Every dev row (8,143, all 9 splits): the v1 request built from it renders byte-identical prompts in both views,
    with the same candidate groups, as decoder_io renders the dev row itself."""
    assert len(rows) == 8143
    kinds = {"carded_noul": 0, "gt26": 0, "choice": 0, "noul": 0}
    for r in rows:
        named = R.parse_v1(R.request_from_row(r))
        assert len(named) == 1
        row = named[0][1]
        assert set(row) == {"state", "instructions", "qtype", "options", "card"}
        items = R.build_items(ro, named)
        assert items[0].perm is None and items[0].text == ro.prompt(r, None) == dio.prompt_texts(ro, [r])[0]
        assert items[0].groups == ro.cand(r)
        if r["qtype"] == "choice":
            rev = list(range(len(r["options"])))[::-1]
            assert len(items) == 2 and items[1].perm == rev and items[1].text == ro.prompt(r, rev)
            assert items[1].groups == ro.cand(r)
            kinds["choice"] += 1
            kinds["gt26"] += len(r["options"]) > 26
        else:
            assert len(items) == 1
            kinds["noul"] += 1
            kinds["carded_noul"] += bool(r.get("card"))
    assert kinds["gt26"] >= 200 and kinds["carded_noul"] >= 2000, kinds


def test_token_ids_match_decoder_io(tok, ro, rows):
    """>= 500 sampled rows (all splits, >26-option rows, carded noul rows): the work items' ids are exactly the ids
    decoder_io.cand_logits feeds the model (batched tokenizer call with truncation, unpadded by the attention mask)."""
    sample = _sample(rows)
    assert len(sample) >= 500 and {r["_split"] for r in sample} == set(T.SPLITS)
    assert sum(len(r["options"] or []) > 26 for r in sample) >= 30
    assert sum(r["qtype"] == "noul" and bool(r.get("card")) for r in sample) >= 40
    for i in range(0, len(sample), 16):
        chunk = sample[i:i + 16]
        items = []
        for r in chunk:
            items += R.build_items(ro, R.parse_v1(R.request_from_row(r)))
        R.tokenize_items(tok, items)
        texts = [it.text for it in items]
        enc = tok(texts, add_special_tokens=False, truncation=True, max_length=dio.MAX_LEN, padding="longest",
                  pad_to_multiple_of=dio.PAD_MULTIPLE, return_tensors="pt")
        for j, it in enumerate(items):
            n = int(enc["attention_mask"][j].sum())
            assert it.n_tokens == n and it.ids == enc["input_ids"][j, :n].tolist()
            assert it.flat == [t for g in it.groups for t in g] and it.sizes == [len(g) for g in it.groups]


def test_cap_matches_tokenizer_truncation(tok):
    text = "alpha beta gamma delta " * 5000  # > MAX_LEN tokens
    full = tok(text, add_special_tokens=False)["input_ids"]
    assert len(full) > dio.MAX_LEN
    ref = tok([text], add_special_tokens=False, truncation=True, max_length=dio.MAX_LEN)["input_ids"][0]
    assert R.cap_ids(full, tok) == ref and len(ref) == dio.MAX_LEN
    it = R.WorkItem(q=0, view=0, perm=None, text=text, groups=[[1]])
    R.tokenize_items(tok, [it])
    assert it.ids == ref and it.n_tokens == dio.MAX_LEN and it.n_raw == len(full)


BAD = [
    ([], "JSON object"),
    ({"questions": {"a": {"type": "noul", "instructions": "?"}}}, "state"),
    ({"state": 3, "questions": {"a": {"type": "noul", "instructions": "?"}}}, "state"),
    ({"state": "x", "questions": {}}, "non-empty"),
    ({"state": "x", "questions": {f"q{i}": {"type": "noul", "instructions": "?"} for i in range(17)}}, "at most 16"),
    ({"state": "x", "questions": {"a": {"type": "score", "instructions": "?"}}}, "type"),
    ({"state": "x", "questions": {"a": {"type": "noul", "instructions": " "}}}, "instructions"),
    ({"state": "x", "questions": {"a": {"type": "noul", "instructions": "?", "options": ["a", "b"]}}}, "no \"options\""),
    ({"state": "x", "questions": {"a": {"type": "choice", "instructions": "?", "options": ["a"]}}}, "2 to 255"),
    ({"state": "x", "questions": {"a": {"type": "choice", "instructions": "?",
                                        "options": [f"o{i}" for i in range(256)]}}}, "2 to 255"),
    ({"state": "x", "questions": {"a": {"type": "choice", "instructions": "?", "options": ["a", "a"]}}}, "duplicate"),
    ({"state": "x", "questions": {"a": {"type": "choice", "instructions": "?", "options": ["a", ""]}}}, "non-empty"),
    ({"state": "x", "questions": {"a": {"type": "choice", "instructions": "?", "options": "ab"}}}, "options"),
    ({"state": "x", "questions": {"a": {"type": "choice", "instructions": "?", "criteria": {"a": None}}}}, "criteria"),
    ({"state": "x", "questions": {"a": {"type": "noul", "instructions": "?", "card": 5}}}, "card"),
    ({"state": "x", "questions": {"a": "noul"}}, "object"),
    ({"state": "x", "foo": 1, "questions": {"a": {"type": "noul", "instructions": "?"}}}, "unknown request field"),
    ({"state": "x", "id": 7, "questions": {"a": {"type": "noul", "instructions": "?"}}}, '"id"'),
]


@pytest.mark.parametrize("req,word", BAD)
def test_parse_errors(ro, req, word):
    with pytest.raises(R.RequestError) as e:
        R.parse_v1(req)
    assert word in str(e.value) and e.value.status == 400 and isinstance(e.value, ValueError)


def test_parse_limits_and_cards(ro):
    q = {f"q{i}": {"type": "noul", "instructions": "?"} for i in range(16)}
    assert len(R.parse_v1({"state": "s", "questions": q})) == 16
    opts = [f"opt {i}" for i in range(255)]
    named = R.parse_v1({"state": "s", "questions": {"c": {"type": "choice", "instructions": "Pick", "options": opts,
                                                          "card": "- opt 3: the third"}}})
    row = named[0][1]
    assert row["card"] == "- opt 3: the third" and len(ro.cand(row)) == 255
    items = R.build_items(ro, named)
    assert "D. opt 3: the third" in items[0].text and f"\n{dio.label(254)}. opt 0\n" in items[1].text
    assert len(dio.label(254)) == 2 and items[1].groups[254] == ro.wide[254]
    assert items[1].text == ro.prompt(row, list(range(255))[::-1])
    noul = R.parse_v1({"state": "s", "questions": {"n": {"type": "noul", "instructions": "OK?",
                                                         "card": "- Yes: fine\n- No: not fine"}}})[0][1]
    t = R.build_items(ro, [("n", noul)])[0].text
    assert "Definitions:\n- Yes: fine\n- No: not fine" in t and "A. Yes: fine" in t


def _tiny_rows(rows):
    """Short dev rows: carded noul, plain noul, choice 3-9 options, choice > 26 options."""
    pick = []
    by = lambda f: sorted([r for r in rows if f(r)], key=lambda r: len(r["state"]) + len(r.get("card") or ""))
    pick += by(lambda r: r["qtype"] == "noul" and r.get("card"))[:2]
    pick += by(lambda r: r["qtype"] == "noul" and not r.get("card"))[:2]
    pick += by(lambda r: r["qtype"] == "choice" and 3 <= len(r["options"]) <= 9)[:3]
    pick += by(lambda r: r["qtype"] == "choice" and len(r["options"]) > 26)[:1]
    return pick


def test_combine_equals_predict_tta_choice(tok, ro, rows):
    """combine() on per-view logits == decoder_io.predict(tta_choice=True) EXACTLY (same per-row logits: batch 1)."""
    model = T.tiny_model()
    sample = _tiny_rows(rows)
    ref = dio.predict(model, tok, sample, batch_size=1, dev="cpu", tta_choice=True)
    for r, p_ref in zip(sample, ref):
        named = R.parse_v1(R.request_from_row(r))
        items = R.build_items(ro, named)
        with torch.no_grad():
            lg = [dio.cand_logits(model, ro, [r], "cpu", perms=[it.perm])[0] for it in items]
        ans, usage = R.combine(named, items, lg)
        a = ans["q0"]
        if r["qtype"] == "noul":
            assert a["noul"] == p_ref["yes"] and a["probabilities"] == {"yes": p_ref["yes"], "no": p_ref["no"]}
        else:
            assert a["probabilities"] == p_ref and list(a["probabilities"]) == r["options"]
            assert a["choice"] == max(p_ref, key=p_ref.get) and a["confidence"] == p_ref[a["choice"]]
        assert a["usage"]["views"] == (2 if r["qtype"] == "choice" else 1)
        assert usage == {"input_tokens": a["usage"]["input_tokens"], "routed_rows": 0}
        # float lists (an SGLang engine's shape) give the same answer
        ans2, _ = R.combine(named, items, [x.tolist() for x in lg])
        assert ans2 == ans


def test_combine_views_and_errors(ro):
    named = R.parse_v1({"state": "s", "questions": {"c": {"type": "choice", "instructions": "?", "options": ["x", "y", "z"]}}})
    items = R.build_items(ro, named)
    a, _ = R.combine(named, items, [torch.tensor([2.0, 0.0, 0.0]), torch.tensor([0.0, 0.0, 2.0])], return_views=True)
    v = a["c"]["view_probabilities"]
    assert v[0]["x"] > 0.7 and v[1]["x"] > 0.7  # view 1 shows x last: its letter C carries the mass
    assert abs(sum(a["c"]["probabilities"].values()) - 1) < 1e-6
    with pytest.raises(ValueError):
        R.combine(named, items, [torch.zeros(3)])
    with pytest.raises(ValueError):
        R.combine(named, items, [torch.zeros(3), torch.zeros(4)])
    one = R.build_items(ro, named, choice_views=1)
    assert len(one) == 1
    a1, _ = R.combine(named, one, [torch.tensor([0.0, 1.0, 0.0])])
    assert a1["c"]["choice"] == "y" and a1["c"]["usage"]["views"] == 1
