"""Regression tests from the A64 fresh L-A build skeptic (18 Oct 2026)."""
import os

import pytest

from LA_COMMON.spans import check_spans
from LA_COMMON.wording import WordingPool
from T53 import blocks
from T53.registry import Registry

POOL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pools", "T53_wording_pool_v1.json")


@pytest.fixture(scope="module")
def specs():
    pool, reg, out = WordingPool.load(POOL), Registry(), []
    for c in blocks.plan():
        out += blocks.build_cell(c, [], pool, reg)
    return out


def test_a_plain_http_transport_defect_is_always_visible_in_the_rendered_string(specs):
    """scp / nc carry no scheme, so a spec whose scheme is http but whose command is scp / nc has an invisible defect and a
    label (ASK) that the string does not support. The skeptic found 28 such rows in the 4,044-row sample."""
    n = 0
    for s in specs:
        if s.egress is not None and s.egress.scheme != "https":
            n += 1
            for r in s.renderings:
                assert "http://" in r["text"], r["text"][:120]
    assert n >= 60


def test_userinfo_urls_never_embed_a_value_with_url_delimiters(specs):
    for s in specs:
        if s.meta.get("channel") == "credential_in_url":
            for r in s.renderings:
                t = r["text"]
                assert t.count("://") == 1 + t.count("postgresql://") + t.count("mysql://") or "@" not in t.split("://", 1)[1].split("/", 1)[0].replace("@", "", 1), t[:140]


def test_all_decision_spans_index_the_slot_text(specs):
    for s in specs:
        turns = [{"text": t.text or ""} for t in s.user_turns]
        assert check_spans(turns, s.decision_spans)
        for sp in s.decision_spans:
            t = s.user_turns[sp["turn"]]
            v = t.slots.get(sp["slot"])
            if v is not None and not str(v).startswith("lex:"):
                assert t.text[sp["start"]:sp["end"]] == v
