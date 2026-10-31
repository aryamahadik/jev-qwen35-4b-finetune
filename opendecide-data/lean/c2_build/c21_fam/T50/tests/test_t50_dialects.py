import copy
import math
import re

import pytest

from LA_COMMON.names import Names
from T50 import dialects as D
from T50.cards import CARD_IDS, make_card

SEEDS = ["dia-a", "dia-b", "dia-c", "d-4", "seed 5", "x"]


def all_cards():
    return [(cid, seed, make_card(cid, Names(seed, provisional=True))) for seed in SEEDS for cid in CARD_IDS]


def atoms_of(card):
    out = set()

    def walk(v):
        if isinstance(v, dict):
            for k, x in v.items():
                out.add(k)
                walk(x)
        elif isinstance(v, (list, tuple)):
            for x in v:
                walk(x)
        elif isinstance(v, str):
            out.add(v)
    walk(card)
    return out


def values_of(card):
    """Every string VALUE of the card (map keys such as the remote names are card data too; slot labels are not)."""
    out = set()
    for k, v in card.items():
        if isinstance(v, str):
            out.add(v)
        elif isinstance(v, list):
            out.update(v)
        elif isinstance(v, dict) and k != "hook_policy":
            for a, b in v.items():
                out.add(a)
                out.update(b if isinstance(b, list) else [b])
        elif isinstance(v, dict):
            out.update(x for f in v.values() for x in (f if isinstance(f, list) else [f]) if isinstance(x, str))
    return out


def test_dialect_ids_and_sets():
    assert D.TRAINED_DIALECTS == ("dialect.json", "dialect.ts", "dialect.yaml", "dialect.md_table", "dialect.prose")
    assert D.HELDOUT_DIALECTS == ("dialect.xml", "dialect.cli_help")
    assert D.ALL_DIALECTS == D.TRAINED_DIALECTS + D.HELDOUT_DIALECTS and len(set(D.ALL_DIALECTS)) == 7
    assert D.is_heldout_dialect("dialect.xml") and not D.is_heldout_dialect("dialect.json")
    assert D.heldout_tag("dialect.cli_help") == "dialect.cli_help" and D.heldout_tag("dialect.yaml") is None


@pytest.mark.parametrize("dialect", D.ALL_DIALECTS)
def test_render_extract_round_trip_for_all_cards_and_seeds(dialect):
    for cid, seed, card in all_cards():
        text = D.render_card_body(dialect, card)
        assert text == D.render_card_body(dialect, copy.deepcopy(card))                  # deterministic, pure
        ex = D.extract_slots(dialect, text)
        assert D.facts_equal(card, ex), (dialect, cid, seed, D.fact_diff(card, ex))
        assert set(ex) == set(card) and ex == card                                         # all 16 keys, same values
        assert card["card_id"] in text and card["display_name"] in text


@pytest.mark.parametrize("dialect", D.ALL_DIALECTS)
def test_every_value_is_rendered_in_full_including_own_config_paths(dialect):
    card = make_card("card.t50.c04", Names("full", provisional=True))
    card["hook_policy"]["own_config_paths"] = ["/srv/x/y/.agent/hook.json", "/srv/x/y/.agent/gate.json"]
    card["trusted_hosts"] = card["trusted_hosts"] + ["extra-host-1.test", "extra-host-2.test"]
    text = D.render_card_body(dialect, card)
    for atom in values_of(card):
        assert atom in text, (dialect, atom)
    for lane in ("contained", "shared", "production"):
        for v in card["context_lists"][lane] + card["database_lists"][lane]:
            assert v in text
    assert D.facts_equal(card, D.extract_slots(dialect, text))
    card["trusted_registries"] = []                                                       # an empty list round-trips too
    assert D.facts_equal(card, D.extract_slots(dialect, D.render_card_body(dialect, card)))


@pytest.mark.parametrize("dialect", D.ALL_DIALECTS)
def test_rendering_adds_nothing_but_card_values_slot_labels_and_generic_structure(dialect):
    vocab = set(D.STRUCTURE_WORDS)
    for k, kind in D.SCHEMA.items():
        vocab |= set(k.split("_"))
        if isinstance(kind, dict):
            for f in kind:
                vocab |= set(f.split("_"))
    for cid, seed, card in all_cards()[:24]:
        text = D.render_card_body(dialect, card)
        atoms = atoms_of(card)
        for tok in re.findall(r"[A-Za-z0-9_./@+~$-]+", text):
            tok = tok.strip(".")
            if tok in atoms or not tok.strip("-$"):
                continue
            for piece in re.split(r"[._/\-$]+", tok):
                assert not piece or piece.lower() in vocab or piece in atoms, (dialect, tok, piece)


@pytest.mark.parametrize("dialect", D.ALL_DIALECTS)
def test_a_changed_value_is_noticed_by_facts_equal(dialect):
    card = make_card("card.t50.c02", Names("mut", provisional=True))
    text = D.render_card_body(dialect, card)
    host = card["trusted_hosts"][0]
    bad = D.extract_slots(dialect, text.replace(host, host + "x"))
    assert not D.facts_equal(card, bad) and D.fact_diff(card, bad) == ["trusted_hosts"]
    flipped = copy.deepcopy(card)
    flipped["ask_on_soft"] = not flipped["ask_on_soft"]
    assert not D.facts_equal(card, D.extract_slots(dialect, D.render_card_body(dialect, flipped)))
    swapped = copy.deepcopy(card)
    swapped["protected_branches"] = list(reversed(swapped["protected_branches"]))          # list order counts
    assert not D.facts_equal(card, swapped)
    # swap-pair cards differ only in the lever slots after the round trip
    other = make_card("card.t50.c01", Names("mut", provisional=True))
    diff = D.fact_diff(card, D.extract_slots(dialect, D.render_card_body(dialect, other)))
    assert set(diff) <= {"card_id", "display_name", "protected_branches", "ask_on_soft", "sudo_policy"}


def test_unparseable_text_and_wrong_dialect_raise_value_error():
    card = make_card("card.t50.c03", Names("bad", provisional=True))
    for d in D.ALL_DIALECTS:
        with pytest.raises(ValueError):
            D.extract_slots(d, "not a card")
        for other in D.ALL_DIALECTS:
            if other != d:
                with pytest.raises(ValueError):
                    D.extract_slots(other, D.render_card_body(d, card))
    with pytest.raises(ValueError):
        D.render_card_body("dialect.nope", card)
    with pytest.raises(ValueError):
        D.extract_slots("dialect.nope", "x")


def test_cards_that_cannot_round_trip_are_refused_not_cut():
    card = make_card("card.t50.c01", Names("ref", provisional=True))
    extra = dict(card, extra_slot="x")
    with pytest.raises(ValueError):
        D.render_card_body("dialect.json", extra)
    missing = {k: v for k, v in card.items() if k != "sudo_listed"}
    with pytest.raises(ValueError):
        D.render_card_body("dialect.json", missing)
    for bad in ("two words", 'quo"te', "a,b", "trailing.", "none", "", "a|b", "a<b"):
        c = copy.deepcopy(card)
        c["allowed_roots"] = c["allowed_roots"] + [bad]
        with pytest.raises(ValueError):
            D.render_card_body("dialect.prose", c)
    c = copy.deepcopy(card)
    c["ask_on_soft"] = "true"
    with pytest.raises(ValueError):
        D.render_card_body("dialect.yaml", c)
    assert not D.facts_equal(card, extra)


def test_json_xml_and_yaml_renderings_are_valid_for_real_parsers():
    import json
    import xml.etree.ElementTree as ET
    card = make_card("card.t50.c06", Names("real", provisional=True))
    obj = json.loads(D.render_card_body("dialect.json", card))
    assert obj["$id"] == card["card_id"] and obj["properties"]["protected_branches"]["const"] == card["protected_branches"]
    root = ET.fromstring(D.render_card_body("dialect.xml", card))
    assert root.get("card_id") == card["card_id"] and len(root.find("allowed_roots")) == len(card["allowed_roots"])
    yaml = pytest.importorskip("yaml")
    y = yaml.safe_load(D.render_card_body("dialect.yaml", card))
    assert y == card


# ------------------------------------------------------------------------------------------------ assignment per group
def test_train_groups_get_only_trained_dialects_each_between_12_and_25_percent():
    ids = ["grp.%d" % i for i in range(2000)]
    shares = D.dialect_shares(ids, "train")
    for d in D.TRAINED_DIALECTS:
        assert 0.12 <= shares[d] <= 0.25, (d, shares[d])
    for d in D.HELDOUT_DIALECTS:
        assert shares[d] == 0.0
    assert all(D.dialect_for_group(g, "train") in D.TRAINED_DIALECTS for g in ids)
    # other id shapes too (specs, quads)
    ids2 = ["T50.quad.%04d" % i for i in range(2000)] + ["T50.pair.%d.c0%d" % (i, i % 8) for i in range(500)]
    shares2 = D.dialect_shares(ids2, "train")
    assert all(0.12 <= shares2[d] <= 0.25 for d in D.TRAINED_DIALECTS)


def test_a_group_always_gets_one_dialect_and_assignment_is_deterministic():
    for g in ("grp.1", "grp.2", "T50.quad.9"):
        first = D.dialect_for_group(g, "train")
        assert all(D.dialect_for_group(g, "train") == first for _ in range(5))      # every member of the pair / quad
        assert D.dialect_for_group(g, "dev") in D.TRAINED_DIALECTS                       # untagged dev: trained dialects
    seen = {D.dialect_for_group("grp.%d" % i, "dev", allow_heldout_dev=True) for i in range(600)}
    assert seen == set(D.ALL_DIALECTS)                                                    # dev may get any of the 7
    assert D.dialect_shares(["g%d" % i for i in range(700)], "dev", allow_heldout_dev=True)["dialect.xml"] > 0.08


def test_heldout_dialect_tags_force_the_dialect_and_a_dev_spec():
    for tag in D.HELDOUT_DIALECTS:
        assert D.dialect_for_group("grp.7", "dev", heldout_family=tag) == tag
        with pytest.raises(ValueError):
            D.dialect_for_group("grp.7", "train", heldout_family=tag)
    # a spec held out for another reason keeps a trained dialect; a train spec can carry no held-out tag at all
    assert D.dialect_for_group("grp.7", "dev", heldout_family="pert.bidi", allow_heldout_dev=True) in D.TRAINED_DIALECTS
    with pytest.raises(ValueError):
        D.dialect_for_group("grp.7", "train", heldout_family="pert.bidi")
    with pytest.raises(ValueError):
        D.dialect_for_group("grp.7", "test")
    # zero held-out dialect in train, over many specs
    assert not any(D.dialect_for_group("s%d" % i, "train") in D.HELDOUT_DIALECTS for i in range(5000))


# ------------------------------------------------------------------------------------------------ token cost
def test_token_cost_per_dialect_is_reported_for_all_seven():
    cards = [c for _, _, c in all_cards()]
    cost = D.token_cost_by_dialect(cards)
    assert set(cost) == set(D.ALL_DIALECTS) and all(v > 100 for v in cost.values())
    text = D.render_card_body("dialect.json", cards[0])
    assert D.est_tokens(text) == math.ceil(len(text) / 3.6)                                  # chars / 3.6, as in gates.py
    rep = D.token_cost_report(cards)
    assert rep["dialect.json"]["pct_over_json"] == 0.0 and set(rep) == set(D.ALL_DIALECTS)
    assert abs(rep["dialect.xml"]["pct_over_json"] - 100 * (cost["dialect.xml"] / cost["dialect.json"] - 1)) < 0.1
    # the XML dialect is the most verbose one (held out, dev only: it does not enter the training cost projection)
    assert max(cost, key=cost.get) == "dialect.xml"
    with pytest.raises(ValueError):
        D.token_cost_by_dialect([])


# ------------------------------------------------------------------------------------------------ scaffold
def test_scaffold_wrap_and_sha_assert():
    assert D.STUB_SCAFFOLD.count(D.PLACEHOLDER) == 1 == D.STUB_SCAFFOLD.count("{{CARD_BODY}}")
    assert "STUB" in D.STUB_SCAFFOLD and D.SCAFFOLD_SHA == D.scaffold_sha(D.STUB_SCAFFOLD) and len(D.SCAFFOLD_SHA) == 64
    import hashlib
    assert D.SCAFFOLD_SHA == hashlib.sha256(D.STUB_SCAFFOLD.encode("utf-8")).hexdigest()
    shas = set()
    for cid, seed, card in all_cards()[:16]:
        for d in D.ALL_DIALECTS:
            body = D.render_card_body(d, card)
            prompt = D.wrap_in_scaffold(body)
            assert D.scaffold_sha_ok(prompt) and D.scaffold_sha_ok(prompt, body=body)
            assert D.unwrap_from_scaffold(prompt) == body == D.unwrap_from_scaffold(D.render_prompt(d, card))
            shas.add(prompt.replace(body, D.PLACEHOLDER))
    assert shas == {D.STUB_SCAFFOLD}                                                       # outside the body: byte-identical
    prompt = D.wrap_in_scaffold("body text")
    assert not D.scaffold_sha_ok(prompt, body="other body")
    for broken in (prompt.replace("STUB", "REAL", 1), prompt + " ", " " + prompt, prompt[:-3], prompt.replace("</policy_card>", "</card>"),
                   D.STUB_SCAFFOLD.replace(D.PLACEHOLDER, ""), "unrelated text"):
        assert not D.scaffold_sha_ok(broken), broken
    # another scaffold (the real one will be L-0's): same functions, its own sha
    real = "SYSTEM: fixed text.\n" + D.PLACEHOLDER + "\nEND."
    assert D.scaffold_sha(real) != D.SCAFFOLD_SHA
    p = D.wrap_in_scaffold("b", real)
    assert D.scaffold_sha_ok(p, real) and not D.scaffold_sha_ok(p) and not D.scaffold_sha_ok(prompt, real)
    with pytest.raises(ValueError):
        D.wrap_in_scaffold("x", "no placeholder")
    with pytest.raises(ValueError):
        D.wrap_in_scaffold("x", D.PLACEHOLDER + D.PLACEHOLDER)
    with pytest.raises(ValueError):
        D.wrap_in_scaffold("has " + D.PLACEHOLDER)
