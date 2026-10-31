import json
import os

import pytest

from T66.solver_b import hook
from helpers import bview, diff_of, merge_ctx, msg_ctx, semver_ctx
from test_merge import REF, TA, TB, VIEW
from test_semver import CALLERS, OLD
from test_msg import DIFFS

ALLOWED_VIEW_KEYS = {"row_id", "head", "sub_block", "rendered", "options", "witness_inputs"}


def test_merge_yes_with_letter_from_rendered_options():
    v = bview("MERGE", merge_ctx("m", VIEW, TA, TB, REF), options=(("A", "NO"), ("B", "YES")))
    r = hook.solver_b(v)
    assert (r["status"], r["label"], r["letter"]) == ("ok", "YES", "B")
    v = bview("MERGE", merge_ctx("m", VIEW, TA, TB, REF), options=(("A", "YES"), ("B", "NO")))
    assert hook.solver_b(v)["letter"] == "A"


def test_semver_vocabulary_and_letter():
    v = bview("SEMVER", semver_ctx("m", OLD, OLD.replace("ValueError", "KeyError"), CALLERS, "major"), options=(("A", "SAFE"), ("B", "BREAKING")))
    r = hook.solver_b(v)
    assert (r["status"], r["label"], r["letter"]) == ("ok", "BREAKING", "B")


def test_msg_ok_and_abstain_shapes():
    v = bview("MSG", msg_ctx(diff_of(DIFFS["CH-10"]), "Tweak the scaling factor in fa"))
    r = hook.solver_b(v)
    assert (r["status"], r["label"]) == ("ok", "YES")
    r2 = hook.solver_b(bview("MSG", msg_ctx(diff_of(DIFFS["CH-10"]), "Misc updates")))
    assert r2["status"] == "abstain" and r2["label"] is None and r2["letter"] is None


def test_wrong_option_vocabulary_is_an_error_not_a_guess():
    v = bview("MERGE", merge_ctx("m", VIEW, TA, TB, REF), options=(("A", "SAFE"), ("B", "BREAKING")))
    assert hook.solver_b(v)["status"] == "error"


def test_option_text_and_list_mismatch_abstains():
    v = bview("MERGE", merge_ctx("m", VIEW, TA, TB, REF))
    v["options"][0]["letter"] = "B"
    assert hook.solver_b(v)["status"] == "abstain"


def test_never_raises_on_garbage():
    for bad in ({}, {"head": "MERGE"}, {"head": "NOPE", "rendered": {}}, {"head": "MERGE", "rendered": {"context": "x", "options_text": "A) YES\nB) NO"}}):
        r = hook.solver_b(bad)
        assert r["status"] in ("error", "abstain") and r["label"] is None


class Tracking(dict):
    def __init__(self, *a, **k):
        dict.__init__(self, *a, **k)
        self.touched = set()

    def __getitem__(self, k):
        self.touched.add(k)
        return dict.__getitem__(self, k)

    def get(self, k, default=None):
        self.touched.add(k)
        return dict.get(self, k, default)

    def __iter__(self):
        self.touched.add("<iter>")
        return dict.__iter__(self)


def test_view_isolation_only_b_view_fields_are_read():
    v = Tracking(bview("MERGE", merge_ctx("m", VIEW, TA, TB, REF)))
    v["gold"], v["spec"], v["meta"] = "NO", {"x": 1}, {"y": 2}           # fields B must never touch
    r = hook.solver_b(v)
    assert r["label"] == "YES"                                              # the planted gold did not matter
    assert v.touched <= ALLOWED_VIEW_KEYS | {"<iter>"} and not ({"gold", "spec", "meta", "label", "manifest", "gold_letter", "names", "slots"} & v.touched)
    assert "<iter>" not in v.touched


def test_real_schema_b_view_is_enough():
    from T66 import schema
    assert set(schema.B_VIEW_FIELDS) == ALLOWED_VIEW_KEYS


def test_adapter_accepts_the_hook():
    from T66 import checked
    ad = checked.adapter(solver_b=hook.solver_b)
    assert ad.solver_b is hook.solver_b
