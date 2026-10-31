"""Check-at-generation (LC_COMMON/checked.py): the owner rule "check each row when it is made" as code. Synthetic rows only; the
stamp service is a test double; nothing generated is executed."""
import copy

import pytest

from LC_COMMON import checked as CK
from LC_COMMON import sandbox_iface as S
from LC_COMMON import suites, tokens
from tool_engine.row_pipeline import RefusingHook, RowGuardRequired, StampServiceRequired, TestDoubleHook

NAMES = {"policy": [], "tool": [], "language": ["python"],
         "runner": ["runner.python_isolated", "runner.twin_counters.python", "runner.domain_enumerator.python"],
         "carrier": ["DOMAIN_DECL", "PROGRAM_PAIR", "QUESTION_FORM", "SRC_FILE"]}


def mkrow(i, label="YES", text=None, pair=None, base="m1", head="EQV2"):
    q = "Do the two versions give the same result?"
    body = text if text is not None else "def f(a):\n    return a + %d" % i
    return {"row_id": "T42c-EQV2-%06d" % i, "family": "T42c", "head": head, "lang": "python", "label": label, "question_form": "T42c-Q-EQV2",
            "carriers": {"QUESTION_FORM": {"form": "T42c-Q-EQV2", "wording_id": "w001", "text": q}}, "prompt_text": body + "\n\n" + q,
            "names": copy.deepcopy(NAMES), "meta": {"pair_id": pair, "base_module": base},
            "manifest": {"solver_a_version": "x", "pins": {"status": "PENDING_L0_IMAGE_RECORD"}}}


def agree_all(row, pk):
    return {"keep": True, "reason": None}


def mk(hook=None, b=agree_all, limit=0.02):
    return CK.RowChecker("T42c", b, hook or TestDoubleHook(), limit, standin=True)


# ------------------------------------------------------------------------------------------------ construction rules
def test_a_checker_cannot_exist_without_a_stamp_hook():
    with pytest.raises(StampServiceRequired):
        CK.RowChecker("T42c", agree_all, None, 0.02, standin=True)
    with pytest.raises(StampServiceRequired):
        CK.RowChecker("T42c", agree_all, RefusingHook(), 0.02, standin=True)


def test_a_production_run_needs_the_guard_and_a_real_hook():
    with pytest.raises(StampServiceRequired):
        CK.RowChecker("T42c", agree_all, TestDoubleHook(), 0.02, standin=False, environ={})
    class Real(CK.StampHook):
        def stamp(self, items):
            return {}
    with pytest.raises(RowGuardRequired):
        CK.RowChecker("T42c", agree_all, Real(), 0.02, standin=False, environ={})


# ------------------------------------------------------------------------------------------------ the stages
def test_clean_rows_are_kept_with_a_complete_stamp():
    ck = mk()
    rows = [mkrow(i, "YES" if i % 2 else "NO") for i in range(6)]
    kept = ck.filter(rows)
    assert len(kept) == 6
    for r in kept:
        st = r["stamp"]
        assert st["generator_sha"] == ck.generator_sha == CK.code_sha("T42c") and st["verdict"] == "clean"
        assert st["answer_checks"]["solver_B"] and st["registry_sha"]


def test_solver_b_disagreement_refusal_and_crash_all_drop_the_row():
    def b(row, pk):
        i = int(row["row_id"][-6:])
        if i == 1:
            return {"keep": False, "reason": "B_label_differs"}
        if i == 2:
            return {"keep": False, "reason": "B_unsupported:construct"}
        if i == 3:
            raise RuntimeError("boom")
        return {"keep": True, "reason": None}
    ck = mk(b=b)
    kept = ck.filter([mkrow(i) for i in range(6)])
    assert [r["row_id"][-1] for r in kept] == ["0", "4", "5"]
    assert ck.dropped[("answer", "B_label_differs")] == 1 and ck.dropped[("answer", "B_refused")] == 2
    assert ck.blocks[0]["block_returns_to_generator"] is True              # 50% dropped for disagreement > the 2% block limit


def test_the_block_rule_is_a_share_of_the_call():
    ck = mk(b=lambda r, pk: {"keep": int(r["row_id"][-6:]) != 0, "reason": "B_label_differs"})
    ck.filter([mkrow(i) for i in range(200)])
    assert ck.blocks[0]["drop_share"] == 0.005 and ck.blocks[0]["block_returns_to_generator"] is False


@pytest.mark.parametrize("bad,code", [("def f(a):\n    return EQ-YES-3", "internal_id"), ("café", "non_ascii"), ("x {lang} y", "unresolved_slot"),
                                      ("see T57 here", "internal_id"), ("x " + CK.R.MARK + " y", "driver_marker"), ("hold \x07 bell", "control_char"),
                                      ("a\n\n\n\n\n\nb", "whitespace_shape")])
def test_format_probe_catches_leaks_and_stray_encodings(bad, code):
    ck = mk()
    assert ck.filter([mkrow(1, text=bad)]) == []
    assert ck.log[0]["detail"] == code


def test_format_probe_allows_tabs_and_test_only_tags_in_standin_but_not_in_production_text():
    assert CK.format_problems(mkrow(1, text="func f() {\n\treturn 1\n}"), standin=False) == []
    r = mkrow(2, text="[TEST-ONLY T42c-Q-EQV2 #3] body")
    assert CK.format_problems(r, standin=False) == ["test_only_wording"] or "test_only_wording" in CK.format_problems(r, standin=False)
    assert "test_only_wording" not in CK.format_problems(r, standin=True)


def test_the_question_must_be_the_last_line():
    r = mkrow(1)
    r["prompt_text"] = "Do the two versions give the same result?\n\nextra"
    assert "question_not_last" in CK.format_problems(r)


def test_names_off_the_allow_list_and_off_the_family_list_drop_the_row():
    ck = mk()
    r1 = mkrow(1)
    r1["names"]["tool"] = ["tool.made_up"]
    r2 = mkrow(2)
    r2["names"]["carrier"] = ["SRC_FILE", "TASK_CARD"]                      # a T57 carrier: on the global list, not on T42c's
    assert ck.filter([r1, r2]) == [] and ck.dropped[("answer", "names_off_allowlist")] == 2


def test_the_token_rule_is_recounted_not_trusted():
    ck = mk()
    big = " ".join("word%d" % i for i in range(1700))
    assert tokens.count(big) > 1536
    r = mkrow(1, text=big)
    r["meta"]["tokens"] = 10                                                # a lying meta field changes nothing
    assert ck.filter([r]) == [] and ck.dropped[("answer", "token_cap")] == 1


def test_malformed_rows_are_dropped():
    ck = mk()
    r = mkrow(1)
    del r["manifest"]["pins"]
    r2 = mkrow(2)
    r2["label"] = ""
    assert ck.filter([r, r2]) == [] and ck.dropped[("answer", "row_malformed")] == 2


# ------------------------------------------------------------------------------------------------ G13
def test_a_g13_hit_drops_the_row_its_partner_and_its_base_module_and_retires_it():
    hook = TestDoubleHook(hit_ids=["T42c-EQV2-000001"])
    ck = mk(hook)
    rows = [mkrow(0, base="mA"), mkrow(1, pair="p1", base="mB"), mkrow(2, pair="p1", base="mB"), mkrow(3, base="mB"), mkrow(4, base="mC")]
    kept = ck.filter(rows)
    assert sorted(r["row_id"][-1] for r in kept) == ["0", "4"]
    assert ck.dropped[("g13", "stamp_hit")] == 1 and ck.dropped[("g13", "stamp_partner_of_hit")] == 2
    assert "mB" in ck.retired
    later = ck.filter([mkrow(9, base="mB")])                                # the retired module never comes back (no re-wording)
    assert later == [] and ck.dropped[("g13", "stamp_partner_of_hit")] == 3


def test_an_exempt_hit_counts_as_clean_and_a_stamp_error_drops():
    ck = mk(TestDoubleHook(exempt_ids=["T42c-EQV2-000001"], error_ids=["T42c-EQV2-000002"]))
    kept = ck.filter([mkrow(0), mkrow(1), mkrow(2)])
    assert [r["row_id"][-1] for r in kept] == ["0", "1"] and ck.dropped[("g13", "stamp_error")] == 1


def test_stamping_goes_in_batches_of_at_most_500_and_only_after_the_answer_checks():
    seen = []
    class Spy(TestDoubleHook):
        def stamp(self, items):
            seen.append([i["row_id"] for i in items])
            return TestDoubleHook.stamp(self, items)
    ck = mk(Spy(), b=lambda r, pk: {"keep": int(r["row_id"][-6:]) % 7 != 0, "reason": "B_label_differs"}, limit=1.0)
    kept = ck.filter([mkrow(i) for i in range(1203)])
    assert all(len(b) <= 500 for b in seen) and len(seen) == 3
    stamped = {x for b in seen for x in b}
    assert all(int(x[-6:]) % 7 != 0 for x in stamped) and len(kept) == len(stamped)    # rows B refused were never sent to G13


def test_the_stamp_items_carry_the_text_to_the_service_but_the_drop_log_never_does():
    got = []
    class Spy(TestDoubleHook):
        def stamp(self, items):
            got.extend(items)
            return TestDoubleHook.stamp(self, items)
    ck = mk(Spy(hit_ids=["T42c-EQV2-000000"]), b=lambda r, pk: {"keep": False, "reason": "B_label_differs"} if r["row_id"].endswith("5") else agree_all(r, pk))
    ck.filter([mkrow(0, text="SECRET_BODY_0"), mkrow(5, text="SECRET_BODY_5"), mkrow(6, text="SECRET_BODY_6")])
    assert got and all(set(i) == {"row_id", "family", "text", "generator_sha"} for i in got)
    assert "SECRET_BODY" not in repr(ck.log) and "SECRET_BODY" not in repr(ck.summary())


# ------------------------------------------------------------------------------------------------ cues
def test_batch_cues_flag_a_length_cue_and_a_label_imbalance_but_never_change_a_row():
    rows = [mkrow(i, "YES", text="x" * (200 + i)) for i in range(120)] + [mkrow(1000 + i, "NO", text="x" * (20 + i)) for i in range(120)]
    before = copy.deepcopy(rows)
    cues = CK.batch_cues(rows)
    assert "length_cue_chars" in cues["EQV2"]["flags"] and cues["EQV2"]["auc_chars"] > 0.9
    assert rows == before
    skew = [mkrow(i, "YES") for i in range(190)] + [mkrow(500 + i, "NO") for i in range(10)]
    assert "label_balance" in CK.batch_cues(skew)["EQV2"]["flags"]


# ------------------------------------------------------------------------------------------------ build-review fixes
def test_a_raising_do_step_fails_the_test_like_every_real_runner():
    ok = ("ok", 3)
    exc = ("exc", "KeyError")
    assert suites.step_ok({"op": "do"}, ok) and not suites.step_ok({"op": "do"}, exc)
    assert suites.step_ok({"op": "eq", "expect": 3}, ok) and not suites.step_ok({"op": "eq", "expect": 3}, exc)
    assert suites.step_ok({"op": "raises", "err": "KeyError"}, exc) and not suites.step_ok({"op": "raises", "err": "KeyError"}, ok)


def test_the_sim_executor_models_a_bare_earlier_call_that_raises_as_a_crashed_driver():
    from LC_COMMON import modgen
    mod, ids = modgen.gen_module(7, "python", "T42c", cdom="cdom01", want_state=True, n_files=1)
    lo = modgen.prepare(mod, "python", ids)
    ops = lo["meta"]["seq"]["domain"]["ops"]
    # an operation that raises on an empty instance, called first and bare, then any final call
    from LC_COMMON.interp import Interp
    for op in ops:
        args = [op["params"][0]["vals"][0]] if op["params"] else []
        if Interp(lo, "python").call(op["fn"], args)[0] == "exc":
            plan = {"calls": [{"fn": op["fn"], "args": args}, {"fn": op["fn"], "args": args}], "mode": "last"}
            res = S.SimExecutor().run([S.driver_request("r", lo, "python", plan)])[0]
            assert res["exit_code"] != 0 and res["stdout"] == ""
            return
    pytest.skip("no raising operation in this module")
