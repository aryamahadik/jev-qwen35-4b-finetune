"""families/T23/test_i2_fixes.py: pilot fix iteration 2 of T23 (PILOT_VERDICT F1, F3), no Haiku, no network.

  F1  extract_fields' ITEM description is the G0 section 10 ruling B2 wording (the name alone, no leading article or
      possessive), stated in the G0_SPEC text itself
  F3  a / an in item slots follows the item's first sound: the table (e-bike, hour, u-lock ...), every pack item, and a
      Mode F note's literal article before its brief item (the note was written for another item)
Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T23/test_i2_fixes.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from families.T23 import plugin as P  # noqa: E402

HERE = Path(__file__).resolve().parent
AN_WORD = re.compile(r"^(?:[aeio]|u(?!ni|se|su|sa|-|til|biq)|hour|honest|honou?r|heir|x-|e-|mp3)", re.I)


def test_item_field_describe_is_the_b2_wording():
    f = {x.name: x for x in P.T23.extract_fields(None, None)}["item"]
    assert f.describe == P.ITEM_FIELD_DESCRIBE
    assert f.describe == ("the item's name alone, with no leading article or possessive "
                          "(a, an, the, my, our, your, his, her, their, its)")
    g0 = " ".join((HERE / "G0_SPEC.md").read_text(encoding="utf-8").split())
    assert "the item's name alone, with no leading article or possessive (a, an, the, my, our, your, his, her, their, its)" in g0
    assert "what the case is about" not in f.describe


@pytest.mark.parametrize("item,art", [
    ("e-bike", "an"), ("E-bike", "an"), ("x-ray pack", "an"), ("hour pass", "an"), ("honest broker plan", "an"),
    ("u-lock", "a"), ("unit plan", "a"), ("university course", "a"), ("one-day pass", "a"), ("euro account", "a"),
    ("laptop", "a"), ("washing machine", "a"), ("office chair", "an"), ("antivirus licence", "an"),
    ("annual plan", "an"), ("umbrella", "an"), ("USB hub", "a"), ("SLA pack", "an"), ("photo editor", "a"),
])
def test_item_article_by_first_sound(item, art):
    assert P.item_article(item) == art


def test_every_pack_item_agrees():
    n = 0
    for pack in P.DOMAINS.values():
        for item in pack.items:
            want = "an" if AN_WORD.match(item) else "a"
            assert P.item_article(item) == want, item
            n += 1
    assert n >= 30


def _note(text, item):
    return K.Skin(skin_id="T23-MF-test", family="T23", text=text,
                  slots=(("CUSTOMER", "name"), ("ITEM", "name")), author_mode="F",
                  brief=(("CUSTOMER", "Dana Okafor"), ("ITEM", item)))


@pytest.mark.parametrize("note_item,row_item,phrase", [
    ("e-bike", "laptop", "about a laptop."), ("laptop", "e-bike", "about an e-bike."),
    ("laptop", "office chair", "about an office chair."), ("e-bike", "washing machine", "about a washing machine."),
    ("office chair", "office chair", "about an office chair."),
])
def test_mode_f_article_follows_the_row_item(note_item, row_item, phrase):
    # the note's own article was written for its own item; the row's item decides
    txt = f"Dana Okafor wrote about a {note_item}."
    sk = _note(txt, note_item)
    filled = P.agree_item_article(sk, row_item).fill(
        {"CUSTOMER": S.name_slot("Dana Okafor"), "ITEM": S.name_slot(row_item)}, {}).text
    assert filled.endswith(phrase), filled
    assert not re.search(r"\ban (?:laptop|washing)|\ba (?:e-bike|office)", filled)


def test_mode_f_leaves_other_determiners_and_mode_t_alone():
    sk = _note("Dana Okafor asked about the e-bike and my e-bike.", "e-bike")
    assert P.agree_item_article(sk, "laptop") is sk
    t = K.Skin(skin_id="T23-SK-x", family="T23", text="About {a|ITEM}.", slots=(("ITEM", "name"),))
    assert P.agree_item_article(t, "laptop") is t
    cap = _note("An e-bike case. Dana Okafor wrote about an e-bike.", "e-bike")
    assert P.agree_item_article(cap, "laptop").text == "A e-bike case. Dana Okafor wrote about a e-bike."
    assert P.agree_item_article(cap, "office chair").text == cap.text      # texts keep the brief item until fill()
