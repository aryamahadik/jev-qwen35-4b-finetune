"""Check-at-generation pipeline (OWNER RULE): the hooks every L-T family wires. In-memory only (stand-in names, a TEST DOUBLE
for the G13 stamp boundary); no row is written, no model is called, no G13 is run."""
import copy
import os
import re
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))          # .../c21_fam
for fam in ("T54", "T55", "T56"):
    p = os.path.join(ROOT, fam)
    if p not in sys.path:
        sys.path.insert(0, p)

import t54_checked  # noqa: E402
import t55_checked  # noqa: E402
import t56_checked  # noqa: E402
from tool_engine import row_pipeline as rp  # noqa: E402
from tool_engine.probe_stub import StubHarness  # noqa: E402

FAMS = {"T54": (t54_checked, 160), "T55": (t55_checked, 160), "T56": (t56_checked, 160)}


@pytest.fixture(scope="module")
def made():
    """One checked run per family with a clean test double: (module, adapter, kept rows, summary)."""
    out = {}
    for fam, (mod, n) in FAMS.items():
        kept, summ, log, rep = mod.run(n, "rp-" + fam, rp.TestDoubleHook(), standin=True)
        out[fam] = (mod, mod.adapter(), kept, summ, log, rep)
    return out


@pytest.mark.parametrize("fam", sorted(FAMS))
def test_no_stamp_hook_means_no_rows(fam):
    mod = FAMS[fam][0]
    with pytest.raises(rp.StampServiceRequired):
        mod.run(20, "x", None, standin=True)
    with pytest.raises(rp.StampServiceRequired):
        mod.run(20, "x", rp.RefusingHook(), standin=True)
    with pytest.raises(rp.StampServiceRequired):
        rp.RefusingHook().stamp([])


@pytest.mark.parametrize("fam", sorted(FAMS))
def test_every_kept_row_carries_a_current_stamp_and_passes_every_answer_check(made, fam):
    mod, ad, kept, summ, log, rep = made[fam]
    assert kept and summ["kept"] == len(kept) and not log
    for r in kept:
        st = r["stamp"]
        assert st["verdict"] == "clean" and st["row_id"] == r["row_id"] and st["generator_sha"] == ad.generator_sha()
        if not r.get("head"):
            assert rp.check_row(r, ad)[0] == [], (r["row_id"], rp.check_row(r, ad))
    assert summ["g13_drop_rate"] == 0 and summ["fix_trigger_g13"] is False
    assert rep["cues"]["ok"], rep["cues"]


@pytest.mark.parametrize("fam", sorted(FAMS))
def test_a_g13_hit_drops_the_whole_pair_retires_the_group_and_refills_with_a_new_scenario(fam):
    mod, n = FAMS[fam]
    kept0, _s, _l, _r = mod.run(n, "rp-hit-" + fam, rp.TestDoubleHook(), standin=True)
    pair_rows = [r for r in kept0 if r.get("pair_role") in ("a", "b") and not r.get("head")]
    victim = pair_rows[0]
    hook = rp.TestDoubleHook(hit_ids={victim["row_id"]})
    kept, summ, log, _rep = mod.run(n, "rp-hit-" + fam, hook, standin=True)
    ids = {r["row_id"] for r in kept}
    assert victim["row_id"] not in ids
    assert not any(r["group_id"] == victim["group_id"] for r in kept)                    # the partner went with it
    assert summ["retired_groups"] >= 1 and summ["refills"] >= 1
    hits = [e for e in log if e["stage"] == "g13"]
    assert hits and all(set(e) <= {"row_id", "group_id", "stage", "reasons", "hits"} for e in hits)    # ids and target names only
    assert any(h["target"] == "target.test" for e in hits for h in e["hits"])
    assert any("~r1" in r["group_id"] for r in kept)                                      # a NEW scenario filled the cell
    assert all(r["stamp"]["verdict"] == "clean" for r in kept)


@pytest.mark.parametrize("fam", sorted(FAMS))
def test_stamp_errors_and_exempt_hits(fam):
    mod, n = FAMS[fam]
    kept0, _s, _l, _r = mod.run(n, "rp-err-" + fam, rp.TestDoubleHook(), standin=True)
    singles = [r for r in kept0 if not r.get("head")]
    a = singles[0]
    b = next(r for r in singles if r["group_id"] != a["group_id"])
    hook = rp.TestDoubleHook(error_ids={a["row_id"]}, exempt_ids={b["row_id"]})
    kept, summ, _log, _rep = mod.run(n, "rp-err-" + fam, hook, standin=True)
    ids = {r["row_id"] for r in kept}
    assert a["row_id"] not in ids                       # an error verdict is never a pass
    assert b["row_id"] in ids                           # a scaffolding-only hit is exempt (R6)
    assert summ["dropped"]


def _first(rows, pred):
    return next(r for r in rows if pred(r) and not r.get("head"))


@pytest.mark.parametrize("fam", sorted(FAMS))
def test_answer_checks_catch_planted_defects(made, fam):
    mod, ad, kept, *_ = made[fam]
    base = _first(kept, lambda r: True)
    other = next(o["label"] for o in base["options"] if o["label"] != base["gold"])

    def broken(**edits):
        r = copy.deepcopy(base)
        for k, v in edits.items():
            r[k] = v
        return r

    # a wrong stored gold: A recompute differs
    assert "A_recompute_differs" in rp.check_row(broken(gold=other), ad)[0]
    # a wrong stored letter: option integrity
    wrong_letter = next(o["letter"] for o in base["options"] if o["letter"] != base["gold_letter"])
    assert "option_integrity" in rp.check_row(broken(gold_letter=wrong_letter), ad)[0]
    # an internal id in the text
    r = copy.deepcopy(base)
    r["rendered"]["text"] = r["rendered"]["text"] + " " + ad.forbidden[0]
    r["rendered"]["options_text"] = r["rendered"]["options_text"] + " " + ad.forbidden[0]
    assert {"internal_leak", "option_integrity"} & set(rp.check_row(r, ad)[0])
    # a name off the allow-list
    r = copy.deepcopy(base)
    r["names"] = dict(r["names"], tool=list(r["names"]["tool"]) + ["verb.made_up"])
    assert "names_off_allowlist" in rp.check_row(r, ad)[0]
    # a lost slot value
    r = copy.deepcopy(base)
    r["slots"] = dict(r.get("slots", {}), zz="never-in-the-text-123")
    assert "slot_lost" in rp.check_row(r, ad)[0]
    # PII and a non-ASCII character in the text
    r = copy.deepcopy(base)
    r["rendered"]["context"] += " mail me at a.b@example.test"
    r["rendered"]["text"] = r["rendered"]["context"] + "\n\n" + r["rendered"]["question"] + "\n" + r["rendered"]["options_text"]
    why = rp.check_row(r, ad)[0]
    assert "pii" in why
    r2 = copy.deepcopy(r)
    r2["rendered"]["context"] = r2["rendered"]["context"].replace("mail me at a.b@example.test", "café")
    r2["rendered"]["text"] = r2["rendered"]["context"] + "\n\n" + r2["rendered"]["question"] + "\n" + r2["rendered"]["options_text"]
    assert "format_probe" in rp.check_row(r2, ad)[0]
    # a text over the token cap
    r = copy.deepcopy(base)
    r["rendered"]["context"] += " word" * 1500
    r["rendered"]["text"] = r["rendered"]["context"] + "\n\n" + r["rendered"]["question"] + "\n" + r["rendered"]["options_text"]
    assert "token_cap" in rp.check_row(r, ad)[0]
    # missing decision spans
    r = copy.deepcopy(base)
    r.pop("decision_spans")
    assert "decision_spans" in rp.check_row(r, ad)[0]


@pytest.mark.parametrize("fam", sorted(FAMS))
def test_solver_b_disagreement_drops_the_row_and_leaves_the_partner_as_an_orphan(fam, monkeypatch):
    mod, n = FAMS[fam]
    real = mod.adapter()
    state = {"victim": None}

    class Flip(object):
        label, letter, abstain, reason = "X", None, None, None

    def solver_b(rec):
        if state["victim"] is None and rec.get("pair_role") == "a" and not rec.get("head"):
            state["victim"] = rec["row_id"]
        if rec["row_id"] == state["victim"]:
            return Flip
        return real.solver_b(rec)

    ad = rp.FamilyAdapter(real.family, real.gen, real.gold_a, solver_b, real.render_b, real.allowlist, real.lint_outputs,
                          real.forbidden, real.abstain_is_drop, real.extra_checks, real.pair_check, real.code_files,
                          compare_reason=real.compare_reason, extra_rows=real.extra_rows, check_extra_row=real.check_extra_row,
                          gates=real.gates)
    kept, summ, log, _rep = rp.run_checked(ad, n, "rp-orph-" + fam, rp.TestDoubleHook(), standin=True)
    v = state["victim"]
    assert v and v not in {r["row_id"] for r in kept}
    assert summ["dropped"].get("answer:A_B_label_differs", 0) >= 1
    partner = [r for r in kept if r["group_id"] == v.rsplit("-", 1)[0] and not r.get("head")]
    assert partner and all(r["orphan"] for r in partner)                                  # the partner STAYS, marked orphan


@pytest.mark.parametrize("fam", sorted(FAMS))
def test_nothing_is_written_and_no_row_text_reaches_the_log(fam, tmp_path, monkeypatch, capsys):
    mod, n = FAMS[fam]
    monkeypatch.chdir(tmp_path)
    hook = rp.TestDoubleHook(hit_ids={"nonexistent"})
    kept, summ, log, rep = mod.run(40, "rp-io-" + fam, hook, standin=True)
    assert list(tmp_path.iterdir()) == []
    assert capsys.readouterr().out == ""
    blob = repr(log) + repr(summ) + repr(rep)
    assert not any(r["rendered"]["context"][:40] in blob for r in kept)


@pytest.mark.parametrize("fam", sorted(FAMS))
def test_the_probe_report_is_wired_to_the_family_gates(fam):
    mod, n = FAMS[fam]
    kept, summ, log, rep = mod.run(n, "rp-probe-" + fam, rp.TestDoubleHook(), standin=True, harness=StubHarness(repeats=2),
                                   probe_min_rows=50)
    assert rep["probes"] and all(set(x) == {"id", "ok"} for x in rep["probes"])


def test_batch_cues_catch_a_planted_position_and_length_cue():
    mod, n = FAMS["T55"]
    kept, *_ = mod.run(700, "rp-cue", rp.TestDoubleHook(), standin=True)
    rows = copy.deepcopy([r for r in kept if r["sub_block"] == "b1_classic"])
    assert len(rows) >= 100
    for r in rows * 2:                                   # plant: the gold option is always the longest
        for o in r["options"]:
            if o["label"] == r["gold"]:
                o["text"] = o["text"] + " (the one to pick)" * 4
    cues = rp.batch_cues(rows * 2, min_rows=100)
    assert not cues["ok"] and any(c["cue"] == "gold_longest" and not c["ok"] for c in cues["cues"])
    for r in rows:                                       # plant: the gold letter is always A
        r["gold_letter"] = "A"
    assert any(c["cue"] == "letter_share" and not c["ok"] for c in rp.batch_cues(rows, min_rows=100)["cues"])


def test_no_executed_code_and_no_network_in_the_pipeline_sources():
    for path in (rp.__file__.replace(".pyc", ".py"), t54_checked.__file__, t55_checked.__file__, t56_checked.__file__):
        src = open(path).read()
        for bad in ("exec(", "eval(", "subprocess", "os.system", "socket", "urllib", "requests", "http.client", "open("):
            assert bad not in src, (os.path.basename(path), bad)
        assert not re.search(r"(?<![\w.])compile\(", src), os.path.basename(path)          # the builtin; re.compile is fine


@pytest.mark.parametrize("fam", sorted(FAMS))
def test_production_runs_only_through_the_row_start_guard_and_stamps_must_carry_the_pinned_registry(fam):
    mod, _n = FAMS[fam]
    ad = mod.adapter()
    env_ok = {"OD_ROWGUARD_FREEZE_SHA": "a" * 64, "OD_ROWGUARD_REGISTRY_SHA": "b" * 64, "OD_ROWGUARD_ALLOWLIST_SHA": ad.allowlist.file_sha}
    with pytest.raises(rp.RowGuardRequired):                                  # no guard variables at all
        rp.run_checked(ad, 20, "g-" + fam, rp.TestDoubleHook(), standin=False, environ={})
    with pytest.raises(rp.RowGuardRequired):                                  # an allow-list that is not the pinned file
        rp.run_checked(ad, 20, "g-" + fam, rp.TestDoubleHook(), standin=False, environ=dict(env_ok, OD_ROWGUARD_ALLOWLIST_SHA="c" * 64))
    kept, summ, log, _rep = rp.run_checked(ad, 40, "g-" + fam, rp.TestDoubleHook(registry_sha="b" * 64), standin=False, environ=env_ok)
    assert kept and all(r["stamp"]["registry_sha"] == "b" * 64 for r in kept)
    assert summ["notes"].get("deny_check_not_wired") == 1                      # production without L-0's deny-list program is noted
    kept2, summ2, _l, _r = rp.run_checked(ad, 40, "g-" + fam, rp.TestDoubleHook(registry_sha="d" * 64), standin=False, environ=env_ok,
                                          max_refill_rounds=0)
    assert not kept2 and summ2["dropped"].get("g13:stamp_error")             # a stamp for another registry is no stamp
    kept3, _s, _l, _r = rp.run_checked(ad, 20, "g-" + fam, rp.TestDoubleHook(registry_sha="b" * 64), standin=False, environ=env_ok,
                                       deny_check=lambda name: False)
    assert kept3


@pytest.mark.parametrize("fam", sorted(FAMS))
def test_overlap_mode_stamps_batch_k_while_batch_k_plus_1_is_made_and_changes_nothing(fam):
    import threading
    mod, _n = FAMS[fam]
    main = threading.current_thread().name

    class Hook(rp.TestDoubleHook):
        threads = set()

        def stamp(self, items):
            Hook.threads.add(threading.current_thread().name)
            return rp.TestDoubleHook.stamp(self, items)

    seq, s1, _l, _r = mod.run(120, "ov-" + fam, Hook(), standin=True, batch_rows=40)
    assert Hook.threads == {main}
    Hook.threads = set()
    ovl, s2, _l, _r = mod.run(120, "ov-" + fam, Hook(), standin=True, batch_rows=40, overlap=True)
    assert Hook.threads - {main}                                              # primary batches were stamped on the worker thread
    assert [r["row_id"] for r in seq] == [r["row_id"] for r in ovl] and s1["stamp_calls"] == s2["stamp_calls"]
