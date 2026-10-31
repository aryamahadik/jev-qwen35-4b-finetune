"""CHECK-AT-CREATION tests for GEN (owner rule 18 Oct 2026): a planted defect in ANY check drops the row (and its pair), a G13 hit drops and
retires the group, and no row can be written without a stamp hook. CPU only; nothing is written; the stamp service is a test double."""
import copy
import json
import re

import pytest

import builder as BU
import gen_common as g
import pool_loader as PL
import row_check as RC
from gen_common import FORMS, GenAllow


@pytest.fixture(scope="module")
def real():
    return PL.load_real_pool()


@pytest.fixture(scope="module")
def vocab():
    return PL.predicate_vocab()


def _builder(real, vocab, seed="rc"):
    return BU.Builder(seed, real, allow=GenAllow(), provisional=False, mode="rows", vocab=vocab, adversary=False)


class Tamper(BU.Builder):
    """A builder that corrupts chosen rows after they are made (to prove the checks bite)."""

    def __init__(self, *a, tamper=None, **k):
        super().__init__(*a, **k)
        self.tamper = tamper or (lambda r: None)

    def unit(self, form, split, index, pair_prob=0.45):
        rows = super().unit(form, split, index, pair_prob)
        for r in rows:
            self.tamper(r)
        return rows


def _tb(real, vocab, tamper, seed="tamper"):
    return Tamper(seed, real, allow=GenAllow(), provisional=False, mode="rows", vocab=vocab, tamper=tamper, adversary=False)


def test_clean_run_keeps_everything_and_stamps(real, vocab):
    b = _builder(real, vocab)
    plan = [(f, "train", 6) for f in FORMS]
    kept, summ, log, cues = RC.build_checked(b, plan, RC.TestDoubleHook(), standin=True)
    assert summ["kept"] == summ["generated"] == len(kept) and not summ["dropped"] and not log
    assert summ["pad_invariance"] == "not_built"
    for r in kept:
        st = r["stamp"]
        assert set(st) == {"row_id", "registry_sha", "method_set_version", "generator_sha", "template_hash", "verdict"}
        assert st["verdict"] == "clean" and st["row_id"] == r["row_id"]
    assert all(r["pair_id"] is None or any(x["pair_id"] == r["pair_id"] and x is not r for x in kept) for r in kept)
    for r in kept:                                  # A1 template-level metadata
        assert r["form"] in r["operator_ids"] and r["template_id"].startswith(r["form"] + "|" + r["carrier"])
        assert r["wording_id"] == "%s#%d" % (r["wording"]["key"], r["wording"]["idx"])
        assert r["error_model_ids"] and "None" not in r["error_model_ids"] and r["level"] is None and r["length_tier"] is None


@pytest.mark.parametrize("name,form,tamper,reason", [
    ("label_flipped", "AR-F1", lambda r: r.__setitem__("label", (r["label"] + 1) % r["k"]), "A_B_answer_differs"),
    ("digit_edited_in_stem", "AR-F1", lambda r: r.__setitem__("stem", re.sub(r"\d", lambda m: str((int(m.group(0)) + 1) % 10), r["stem"], count=1)), ("parse_back", "B_reject", "A_B_answer_differs", "B_parse_fail", "decision_spans")),
    ("cve_literal", "LG-L1", lambda r: r.__setitem__("stem", r["stem"] + " See CVE-2024-12345."), "guard_literal"),
    ("email", "TM-T1", lambda r: r.__setitem__("stem", r["stem"] + " a@b.example"), "pii"),
    ("unfilled_slot", "CA-C3", lambda r: r.__setitem__("stem", r["stem"] + " {target}"), "unfilled_slot"),
    ("non_ascii", "TB-B1", lambda r: r.__setitem__("stem", r["stem"].replace("\n", " é\n", 1)), "format_probe"),
    ("weight_upweighted", "CA-C1", lambda r: r.__setitem__("weight", 2.0), "weight"),
    ("pad_field", "CA-C2", lambda r: r.__setitem__("pad", [1]), "pad_present"),
    ("span_offset", "AR-F2", lambda r: r["decision_spans"][0].__setitem__("start", r["decision_spans"][0]["start"] + 1), "decision_spans"),
    ("token_cap", "TM-T2", lambda r: r.__setitem__("tokens_est", 1600), "token_cap"),
    ("carrier_off_list", "LG-L2", lambda r: r.__setitem__("carrier", "TXT-FANCY"), "names_off_allowlist"),
    ("unit_off_list", "AR-F1", lambda r: r["spec"]["base"][0].__setitem__("unit", "furlong"), "names_off_allowlist"),
])
def test_planted_defect_drops_the_row_and_its_pair(real, vocab, name, form, tamper, reason):
    hit = {"n": 0}

    def t(r):
        if r["row_id"].endswith("-00001"):
            hit["n"] += 1
            tamper(r)
    b = _tb(real, vocab, t)
    kept, summ, log, _ = RC.build_checked(b, [(form, "train", 4)], RC.TestDoubleHook(), standin=True)
    assert hit["n"] == 1
    dropped_ids = {l["row_id"] for l in log if l["stage"] == "answer"}
    assert dropped_ids, name
    flat = [x for l in log for x in l["reasons"]]
    if reason:
        assert set(flat) & set(reason if isinstance(reason, tuple) else (reason,)), (name, flat)
    # the unit that failed is gone as a whole and was re-made: the cell is not short
    assert not summ["cells_short"] and summ["refills"] >= 1
    assert not (dropped_ids & {r["row_id"] for r in kept})
    for r in kept:
        if r["pair_id"]:
            assert sum(1 for x in kept if x["pair_id"] == r["pair_id"]) == 2


def test_a_g13_hit_drops_the_whole_pair_and_retires_the_group(real, vocab):
    b = _builder(real, vocab, "g13")
    probe = [r for i in range(10) for r in _builder(real, vocab, "g13").unit("AR-F1", "train", i, pair_prob=1.0)]
    hit_id = next(r["row_id"] for r in probe if r["pair_id"] and r["pair_role"] == "a")
    stamper = RC.TestDoubleHook(hit_ids=[hit_id])
    kept, summ, log, _ = RC.build_checked(b, [("AR-F1", "train", 10)], stamper, standin=True, pair_prob=1.0)
    g13 = [l for l in log if l["stage"] == "g13"]
    assert len(g13) == 2 and summ["retired_groups"] == 1
    assert {l["reasons"][0] for l in g13} == {"g13_hit", "pair_partner_of_hit"}
    assert hit_id not in {r["row_id"] for r in kept}
    # the log carries ids, reason codes and target / method names only: never text
    dumped = json.dumps(log)
    assert "target.test" in dumped and "stem" not in dumped and "options" not in dumped
    assert all(r["stamp"]["verdict"] == "clean" for r in kept)


def test_scaffolding_exempt_hit_is_clean(real, vocab):
    b = _builder(real, vocab, "exempt")
    first = next(r["row_id"] for r in _builder(real, vocab, "exempt").unit("LG-L1", "train", 0, pair_prob=0.0))
    kept, summ, log, _ = RC.build_checked(b, [("LG-L1", "train", 3)], RC.TestDoubleHook(exempt_ids=[first]), standin=True, pair_prob=0.0)
    assert not log and summ["kept"] == 3


def test_stamp_error_drops_like_a_hit(real, vocab):
    b = _builder(real, vocab, "err")
    first = next(r["row_id"] for r in _builder(real, vocab, "err").unit("CA-C5", "train", 0, pair_prob=0.0))
    kept, summ, log, _ = RC.build_checked(b, [("CA-C5", "train", 3)], RC.TestDoubleHook(error_ids=[first]), standin=True, pair_prob=0.0)
    assert [l["reasons"] for l in log] == [["stamp_error"]]


def test_no_hook_no_rows(real, vocab):
    b = _builder(real, vocab)
    with pytest.raises(RC.StampServiceRequired):
        RC.build_checked(b, [("AR-F1", "train", 2)], None)
    with pytest.raises(RC.StampServiceRequired):
        RC.build_checked(b, [("AR-F1", "train", 2)], RC.RefusingHook())


def test_production_needs_guard_conformance_template_hash_and_a_real_hook(real, vocab):
    b = _builder(real, vocab)
    with pytest.raises(RC.StampServiceRequired):          # a test double cannot stamp a production run
        RC.build_checked(b, [("AR-F1", "train", 1)], RC.TestDoubleHook(), standin=False)

    class Real(RC.StampHook):
        def stamp(self, items):
            return {}
    with pytest.raises(RC.RowGuardRequired):              # not started through the row-start guard
        RC.build_checked(b, [("AR-F1", "train", 1)], Real(), standin=False, environ={})
    env = {"OD_ROWGUARD_FREEZE_SHA": "f" * 64, "OD_ROWGUARD_REGISTRY_SHA": "1" * 64, "OD_ROWGUARD_ALLOWLIST_SHA": b.allow.sha}
    with pytest.raises(RC.ConformanceRecordRequired):
        RC.build_checked(b, [("AR-F1", "train", 1)], Real(), standin=False, environ=env)
    with pytest.raises(RC.TemplateHashStale):
        RC.build_checked(b, [("AR-F1", "train", 1)], Real(), standin=False, environ=env, conformance_ok=lambda sha: True,
                         template_hash="a", template_hash_live="b")
    dry = BU.Builder("x", g.make_testonly_pool(), allow=GenAllow(), provisional=True, mode="dry")
    with pytest.raises(RC.RowGuardRequired):              # dry builder / test pool / provisional names
        RC.build_checked(dry, [("AR-F1", "train", 1)], Real(), standin=False, environ=env)


def test_a_stamp_from_another_registry_is_no_stamp(real, vocab):
    b = _builder(real, vocab, "reg")
    env = {"OD_ROWGUARD_FREEZE_SHA": "f" * 64, "OD_ROWGUARD_REGISTRY_SHA": "1" * 64, "OD_ROWGUARD_ALLOWLIST_SHA": b.allow.sha}

    class Other(RC.StampHook):
        registry_sha = "2" * 64

        def stamp(self, items):
            return {i["row_id"]: {"verdict": "clean", "hits": [], "registry_sha": "2" * 64, "method_set_version": "v"} for i in items}
    kept, summ, log, _ = RC.build_checked(b, [("AR-F1", "train", 2)], Other(), standin=False, environ=env, conformance_ok=lambda sha: True,
                                          template_hash="h", template_hash_live="h", max_refill_rounds=0, pair_prob=0.0)
    assert not kept and summ["dropped"].get("g13:stamp_error") == 2


def test_batches_are_at_most_500_rows(real, vocab):
    b = _builder(real, vocab, "batch")
    sizes = []

    class Count(RC.TestDoubleHook):
        def stamp(self, items):
            sizes.append(len(items))
            return super().stamp(items)
    RC.build_checked(b, [("AR-F2", "train", 420), ("CA-C1", "train", 300)], Count(), standin=True)
    assert sizes and max(sizes) <= 500 and sum(sizes) >= 700


def test_batch_cues_flag_a_planted_letter_skew(real, vocab):
    b = _builder(real, vocab, "cues")
    kept, _s, _l, cues = RC.build_checked(b, [("AR-F1", "train", 260)], RC.TestDoubleHook(), standin=True)
    assert cues["ok"]
    skew = copy.deepcopy(kept)
    for r in skew:
        r["label"] = 0
    assert not RC.batch_cues(skew)["ok"]
