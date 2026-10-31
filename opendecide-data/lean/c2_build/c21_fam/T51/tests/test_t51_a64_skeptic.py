"""Regression tests from the A64 fresh L-A build skeptic (18 Oct 2026)."""
import os

import pytest

from LA_COMMON.spans import check_spans
from LA_COMMON.wording import WordingPool
from T51 import blocks

POOL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pools", "T51_wording_pool_v1.json")


@pytest.fixture(scope="module")
def specs():
    pool, out = WordingPool.load(POOL), []
    for c in blocks.plan():
        out += blocks.build_cell(c, [], pool)
    return out


def test_all_decision_spans_index_the_slot_text_after_every_member_of_a_pair_is_rendered(specs):
    """A Turn object shared by the pos and neg members of a trajectory pair used to be re-rendered by the second member:
    the first member kept spans for a wording it no longer showed (about 100 rows)."""
    for s in specs:
        turns = [{"text": t.text or ""} for t in s.user_turns]
        assert check_spans(turns, s.decision_spans)
        for sp in s.decision_spans:
            t = s.user_turns[sp["turn"]]
            v = t.slots.get(sp["slot"])
            if v is not None and not str(v).startswith("lex:"):
                assert t.text[sp["start"]:sp["end"]] == v, (s.spec_id, t.form)


def test_pair_members_do_not_share_turn_objects_and_a_shared_turn_is_worded_identically(specs):
    by = {}
    for s in specs:
        by.setdefault(s.group, []).append(s)
    shared = 0
    for g, ms in by.items():
        ids = [id(t) for m in ms for t in m.user_turns]
        assert len(ids) == len(set(ids)), g
        if len(ms) == 2 and ms[0].meta.get("variant", "").startswith("traj_") and ms[1].meta.get("variant") == "traj_revoked_boundary":
            pos, neg = ms
            assert neg.user_turns[0].text == pos.user_turns[0].text
            shared += 1
    assert shared >= 10
