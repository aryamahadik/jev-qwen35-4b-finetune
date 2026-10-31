"""families/T32/test_plugin.py: in-memory tests for the T32 plugin (A37 f: nothing is written; no Haiku, no network).

  contract        validate_plugin(strict) == [], solver-B independence, G0-lite frozen and <= 200 lines
  semantics       a hand-built table of small chats (one per G0 R9 rule and section 8 ambiguity point), built without the
                  sampler, answered by both solvers through the rendered row
  G2 / G3         solver A == solver B and parse == canonical on 5,000 sampled specs (+ every complement form)
  pipeline        every kit program gate (G2, G3, G4, G-SL, G-LEX, G-TW, schema; G15 on a slice) on 750 units, and
                  the spec 4.1 overlay shares
  relations       twins differ in exactly one input slot and the gold moves as the construction predicted;
                  complements opposite; G4 metamorphic predictions hold
  balance         gold labels inside the G0 section 4 bands on 2,000 specs; trap floors; depth; gold positions
  G-SL            the built-in placeholder skins, wordings and attack notes lint clean; message forms carry no status
                  or label word; no literal value or gold-label word outside the slots of any rendered row
  length          approx tokens <= 2,000 on every row; real-token mean <= 800 (local Qwen tokenizer)
  determinism     same seed -> same spec and rows
  injected bugs   G2, G3, G-TW and G-SL catch a broken solver B, solver A, renderer, twin prediction and skin; solver B
                  refuses rows that break a G0 R10 invariant
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T32
"""
from __future__ import annotations

import collections
import dataclasses
import datetime as dt
import hashlib
import os
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import gsl, paths, pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.distractors import position_counts  # noqa: E402
from c2_kit.plugin import Spec  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from c2_kit import cards as CD  # noqa: E402
from families.T32 import fixtures as FX  # noqa: E402
from families.T32 import packs_v2 as PV  # noqa: E402
from families.T32 import plugin as P  # noqa: E402
from families.T32 import solver_b as B  # noqa: E402
from families.T32 import vocab as V  # noqa: E402

SAMPLERS = P.T32.SAMPLERS
TRAINING = tuple(s for s in SAMPLERS if s not in P.T32.HELD_OUT_SAMPLERS)
COMPLEMENT_FORMS = {q: tuple(f for f, _w in fs) for q, fs in P.COMPLEMENTS.items()}
YN_BASE = ("yn_broken", "yn_dneg_broken", "yn_kept", "yn_kept_vs")
TOKENIZER = Path(os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/"
                                    "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json"))


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    """On the 6 stand-in packs: the frozen packs are exercised by test_pilot_fixes.py and the pilot (F7)."""
    return P.T32(lexicon=ctx.lexicon, vocab=PV.standin())


@pytest.fixture(scope="module")
def specs(plugin):
    """2,000 specs: seeds 0-399 (whole seed pairs) x 5 samplers."""
    return [plugin.sample(seed, smp) for seed in range(400) for smp in SAMPLERS]


def _check_row(plugin, ctx, spec, rr):
    """G2 + G3 on one rendered row: parse == canonical, solver B == solver A, options read back to their keys."""
    view = plugin.parse(rr.row, ctx)
    facts = {k: v for k, v in view.items() if k != "options"}
    assert facts == plugin.canonical_for(spec, rr.row["meta"]["c2"]["author_mode"]), (spec.seed, spec.sampler)
    gold = plugin.solve_a(spec)
    assert plugin.solve_b(view) == gold == rr.answer, (spec.seed, spec.sampler, spec.qform)
    if rr.row["qtype"] == "choice":
        assert view["options"][rr.row["options"].index(rr.row["gold"])] == gold
        assert len(set(view["options"])) == len(view["options"])
    return view


# ------------------------------------------------------------------------------------------------ hand-built chats

D = dt.date


def _hand_spec(plugin, lines, *, asof, who="Lee", task="return_drill", members=("Ana", "Lee", "Mo"), auth=None,
               qform="ch_status", style="chat"):
    """A spec built by hand (not by the sampler). lines: (date, sender, to, sem, {form slot: value}); TASK and COND
    values are vocab keys. The asked commitment's slots keep the plugin's names (TASK0, DUE0, NEWDUE0, COND0)."""
    reg = plugin.lexicon
    sl, msgs = {}, []
    tasks = {k: [v] for k, v in V.TASKS.items()}
    conds = {k: [v] for k, v in V.CONDS.items()}
    asked_cond = next((a.get("COND") for _d, s, _t, sem, a in lines
                       if sem in P.COMMIT_SEMS and s == who and a["TASK"] == task), None)
    for i, (day, spk, to, sem, args) in enumerate(lines):
        mine = args.get("TASK") == task or (asked_cond is not None and args.get("COND") == asked_cond)
        bind = {}
        for fs, v in sorted(args.items()):
            if fs == "TASK":
                name = "TASK0" if v == task else f"L{i}_TASK"
                sl[name] = S.category_slot(v, tasks)
            elif fs == "COND":
                name = "COND0" if mine else f"L{i}_COND"
                sl[name] = S.category_slot(v, conds)
            elif fs == "DUE":
                name = ("DUE0" if sem in P.COMMIT_SEMS else "TRY0") if mine else f"L{i}_DUE"
                sl[name] = S.date_slot(v)
            else:
                name = "NEWDUE0" if mine else f"L{i}_NEW_DUE"
                sl[name] = S.date_slot(v)
            bind[fs] = name
        role = {"chat.commit": "commit", "chat.commit_if": "commit", "chat.cond_met": "cond", "chat.cond_off": "cond",
                "chat.ext_yes": "ext_reply", "chat.ext_no": "ext_reply"}.get(sem, sem.split(".")[1])
        sl[f"T{i}"], sl[f"S{i}"] = S.date_slot(day), S.name_slot(spk)
        if to:
            sl[f"A{i}"] = S.name_slot(to)
        sl[f"M{i}"] = reg.clause(plugin._forms_of(sem)[0], bind=bind)
        c = 0 if mine and role != "ack" else (i + 1 if role == "commit" else None)
        msgs.append({"role": role, "c": c, "to": to is not None, "bind": dict(sorted(bind.items()))})
    for j, m in enumerate(members):
        sl[f"P{j}"] = S.name_slot(m)
    if auth:
        sl["AUTH"] = S.name_slot(auth)
    sl["WHO"], sl["QTASK"], sl["ASOF"] = S.name_slot(who), S.category_slot(task, tasks), S.date_slot(asof)
    sl["TOPIC"] = S.category_slot("house_move", {k: [v] for k, v in V.TOPICS.items()})
    sl["OWNER"] = S.name_slot(members[0])
    st = {"style": style, "auth": auth is not None, "n_members": len(members), "msgs": msgs}
    return Spec("T32", "S1", 0, "T32:S1:hand", qform, sl, structure=st, pack="t32:home")


def _both(plugin, ctx, spec):
    """(solver A, solver B through the rendered and parsed row) for a hand spec."""
    rr = plugin.render(spec, ctx)
    view = _check_row(plugin, ctx, spec, rr)
    return plugin.solve_a(spec), plugin.solve_b(view)


C = ("chat.commit", {"TASK": "return_drill", "DUE": D(2026, 3, 10)})
DONE = ("chat.done", {"TASK": "return_drill"})
HAND = [   # (name, lines after the commitment line, asof, auth, expected status) -- G0 R9 / section 8
    ("done on the due date is kept (8.1)", [(D(2026, 3, 10), "Lee", "Ana", *DONE)], D(2026, 3, 12), None, "kept"),
    ("done the day after is broken (8.1, 8.8)", [(D(2026, 3, 11), "Lee", "Ana", *DONE)], D(2026, 3, 12), None,
     "broken"),
    ("status date on the due date: not yet due (8.2)", [], D(2026, 3, 10), None, "not_yet_due"),
    ("status date the day after: broken", [], D(2026, 3, 11), None, "broken"),
    ("done after the status date is ignored (8.7)", [(D(2026, 3, 9), "Lee", "Ana", *DONE)], D(2026, 3, 8), None,
     "not_yet_due"),
    ("take back alone breaks it before the due date (8.4)",
     [(D(2026, 3, 5), "Lee", "Ana", "chat.retract", {"TASK": "return_drill"})], D(2026, 3, 6), None, "broken"),
    ("take back then the promisee lets him off: waived (8.4)",
     [(D(2026, 3, 5), "Lee", "Ana", "chat.retract", {"TASK": "return_drill"}),
      (D(2026, 3, 6), "Ana", "Lee", "chat.release", {"TASK": "return_drill"})], D(2026, 3, 7), None, "waived"),
    ("a third member's release does nothing (8.5)",
     [(D(2026, 3, 6), "Mo", "Lee", "chat.release", {"TASK": "return_drill"})], D(2026, 3, 7), None, "not_yet_due"),
    ("the pinned AUTH may release", [(D(2026, 3, 6), "Mo", "Lee", "chat.release", {"TASK": "return_drill"})],
     D(2026, 3, 7), "Mo", "waived"),
    ("an allowed yes moves the due date", [
        (D(2026, 3, 8), "Lee", "Ana", "chat.ext_ask", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)}),
        (D(2026, 3, 9), "Ana", "Lee", "chat.ext_yes", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)}),
        (D(2026, 3, 13), "Lee", "Ana", *DONE)], D(2026, 3, 15), None, "kept"),
    ("a yes from a third member moves nothing (8.5)", [
        (D(2026, 3, 8), "Lee", "Ana", "chat.ext_ask", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)}),
        (D(2026, 3, 9), "Mo", "Lee", "chat.ext_yes", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)}),
        (D(2026, 3, 13), "Lee", "Ana", *DONE)], D(2026, 3, 15), None, "broken"),
    ("an unanswered request moves nothing", [
        (D(2026, 3, 8), "Lee", "Ana", "chat.ext_ask", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)})],
     D(2026, 3, 12), None, "broken"),
    ("a refused request moves nothing", [
        (D(2026, 3, 8), "Lee", "Ana", "chat.ext_ask", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)}),
        (D(2026, 3, 9), "Ana", "Lee", "chat.ext_no", {"TASK": "return_drill"})], D(2026, 3, 12), None, "broken"),
    ("a release after a later allowed yes uses the new date", [
        (D(2026, 3, 8), "Lee", "Ana", "chat.ext_ask", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)}),
        (D(2026, 3, 10), "Ana", "Lee", "chat.ext_yes", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)}),
        (D(2026, 3, 13), "Ana", "Lee", "chat.release", {"TASK": "return_drill"})], D(2026, 3, 13), None, "waived"),
    ("an allowed yes: a status date between the two dates is not yet due (H4)", [
        (D(2026, 3, 8), "Lee", "Ana", "chat.ext_ask", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)}),
        (D(2026, 3, 9), "Ana", "Lee", "chat.ext_yes", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)})],
     D(2026, 3, 12), None, "not_yet_due"),
    ("let off, then done on time: waived, the first status that fits (H3)", [
        (D(2026, 3, 6), "Ana", "Lee", "chat.release", {"TASK": "return_drill"}),
        (D(2026, 3, 8), "Lee", "Ana", *DONE)], D(2026, 3, 9), None, "waived"),
    ("a pinned AUTH who is the maker adds nobody: his own yes moves nothing (H1)", [
        (D(2026, 3, 8), "Lee", "Ana", "chat.ext_ask", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)}),
        (D(2026, 3, 9), "Lee", "Ana", "chat.ext_yes", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)}),
        (D(2026, 3, 13), "Lee", "Ana", *DONE)], D(2026, 3, 15), "Lee", "broken"),
    ("a pinned AUTH who is the maker: the promisee may still let him off (H1)",
     [(D(2026, 3, 6), "Ana", "Lee", "chat.release", {"TASK": "return_drill"})], D(2026, 3, 7), "Lee", "waived"),
    ("an unrelated task's lines do nothing", [
        (D(2026, 3, 4), "Ana", "Lee", "chat.commit", {"TASK": "water_plants", "DUE": D(2026, 3, 5)}),
        (D(2026, 3, 6), "Ana", "Lee", "chat.retract", {"TASK": "water_plants"}),
        (D(2026, 3, 7), "Lee", "Ana", "chat.release", {"TASK": "water_plants"})], D(2026, 3, 8), None,
     "not_yet_due"),
]
COND = ("chat.commit_if", {"COND": "street_party", "TASK": "return_drill", "DUE": D(2026, 3, 10)})
HAND_COND = [
    ("no line on the event, past the due date: not triggered (8.6)", [], D(2026, 3, 20), "not_triggered"),
    ("event called off: not triggered", [(D(2026, 3, 4), "Mo", None, "chat.cond_off", {"COND": "street_party"})],
     D(2026, 3, 8), "not_triggered"),
    ("event going ahead after the status date: not triggered (8.7)",
     [(D(2026, 3, 6), "Mo", None, "chat.cond_met", {"COND": "street_party"})], D(2026, 3, 5), "not_triggered"),
    ("event going ahead, then done: kept", [(D(2026, 3, 4), "Mo", None, "chat.cond_met", {"COND": "street_party"}),
                                            (D(2026, 3, 9), "Lee", "Ana", *DONE)], D(2026, 3, 12), "kept"),
    ("event going ahead, nothing done: broken after the due date",
     [(D(2026, 3, 4), "Mo", None, "chat.cond_met", {"COND": "street_party"})], D(2026, 3, 11), "broken"),
]


@pytest.mark.parametrize("name, after, asof, auth, want", HAND, ids=[h[0] for h in HAND])
def test_hand_built_semantics(plugin, ctx, name, after, asof, auth, want):
    lines = [(D(2026, 3, 3), "Lee", "Ana", *C)] + after
    for qform in ("ch_status", "yn_broken", "yn_kept"):
        spec = _hand_spec(plugin, lines, asof=asof, auth=auth, qform=qform)
        a, b = _both(plugin, ctx, spec)
        assert a == b == plugin._answer_of(qform, want, None), (name, qform, a, b)
    assert plugin._plan_status(plugin._plan(_hand_spec(plugin, lines, asof=asof, auth=auth))) == want


@pytest.mark.parametrize("name, after, asof, want", HAND_COND, ids=[h[0] for h in HAND_COND])
def test_hand_built_conditions(plugin, ctx, name, after, asof, want):
    lines = [(D(2026, 3, 3), "Lee", "Ana", *COND)] + after
    a, b = _both(plugin, ctx, _hand_spec(plugin, lines, asof=asof))
    assert a == b == want, (name, a, b)


def test_hand_built_try_is_not_a_commitment(plugin, ctx):
    """'I'll try' by the 5th, then a real commitment by the 10th, done on the 8th: kept (8.3)."""
    lines = [(D(2026, 3, 1), "Lee", "Ana", "chat.try", {"TASK": "return_drill", "DUE": D(2026, 3, 5)}),
             (D(2026, 3, 3), "Lee", "Ana", *C), (D(2026, 3, 8), "Lee", "Ana", *DONE)]
    spec = _hand_spec(plugin, lines, asof=D(2026, 3, 9))
    assert _both(plugin, ctx, spec) == ("kept", "kept")
    assert plugin._fold(spec, f=frozenset({"try_commit"}))[0] == "broken"       # the named error model differs


def test_hand_built_due_date_question(plugin, ctx):
    lines = [(D(2026, 3, 3), "Lee", "Ana", *C),
             (D(2026, 3, 8), "Lee", "Ana", "chat.ext_ask", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)}),
             (D(2026, 3, 9), "Mo", "Lee", "chat.ext_yes", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)}),
             (D(2026, 3, 4), "Ana", "Mo", "chat.commit", {"TASK": "water_plants", "DUE": D(2026, 3, 6)})]
    lines = sorted(lines, key=lambda x: x[0])
    for auth, want in ((None, "2026-03-10"), ("Mo", "2026-03-14")):
        spec = _hand_spec(plugin, lines, asof=D(2026, 3, 9), auth=auth, qform="ch_due")
        assert _both(plugin, ctx, spec) == (want, want)


def test_solver_b_refuses_invariant_breaks(plugin, ctx):
    """G0 R10: a done from someone else, a release by the maker, a done before the event goes ahead."""
    bad = [
        [(D(2026, 3, 3), "Lee", "Ana", *C), (D(2026, 3, 5), "Ana", "Lee", *DONE)],
        [(D(2026, 3, 3), "Lee", "Ana", *C), (D(2026, 3, 5), "Lee", "Ana", "chat.release", {"TASK": "return_drill"})],
        [(D(2026, 3, 3), "Lee", "Ana", *COND), (D(2026, 3, 5), "Lee", "Ana", *DONE)],
        [(D(2026, 3, 3), "Lee", "Ana", *C), (D(2026, 3, 12), "Ana", "Lee", "chat.ext_yes",
                                             {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 14)})],
        # v2 (Haiku pass): a self-addressed commitment (H2), a date not later than its own line (H14), two requests
        # for more time (H7, H8), an event line on the first date (H12)
        [(D(2026, 3, 3), "Lee", "Lee", *C)],
        [(D(2026, 3, 3), "Lee", "Ana", "chat.commit", {"TASK": "return_drill", "DUE": D(2026, 3, 3)})],
        [(D(2026, 3, 3), "Lee", "Ana", *C),
         (D(2026, 3, 5), "Lee", "Ana", "chat.ext_ask", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 12)}),
         (D(2026, 3, 6), "Lee", "Ana", "chat.ext_ask", {"TASK": "return_drill", "NEW_DUE": D(2026, 3, 13)})],
        [(D(2026, 3, 3), "Lee", "Ana", *COND), (D(2026, 3, 10), "Mo", None, "chat.cond_met", {"COND": "street_party"})],
    ]
    for lines in bad:
        spec = _hand_spec(plugin, lines, asof=D(2026, 3, 13))
        rr = plugin.render(spec, ctx)
        with pytest.raises(B.Refused):
            B.solve_b(plugin.parse(rr.row, ctx))
        assert any(g == "G2" for g, _ in pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False))


# ------------------------------------------------------------------------------------------------ contract

def test_plugin_meets_the_strict_contract(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []
    assert plugin.PARADIGM_A != plugin.PARADIGM_B
    g0 = Path(plugin.G0_LITE)
    assert len(g0.read_text(encoding="utf-8").splitlines()) <= 200
    assert hashlib.sha256(g0.read_bytes()).hexdigest() == plugin.G0_SHA256


def test_solver_b_shares_no_code_with_solver_a():
    src = Path(B.__file__).read_text(encoding="utf-8")
    assert "families.T32.plugin" not in src and "c2_kit.rules" not in src and "glob_a" not in src
    for name in KP.B_FORBIDDEN_NAMES:
        assert not re.search(rf"\b{name}\b", src), name
    assert "sqlite3" in src and "CASE" in src                     # the declarative paradigm (G0 R16)


def test_solver_b_keeps_its_own_copy_of_the_card(plugin):
    for card_style in P.CARD_SHARES:
        for style in ("chat", "log"):
            for auth in (False, True):
                spec = plugin.sample(0, "S1")
                spec = spec.replace(structure={**spec.structure, "style": style, "auth": auth},
                                    slots={**spec.slots, "AUTH": S.name_slot("Ana")})
                text = K.fill(plugin.card_template(spec, card_style), spec.all_slots()).text
                m = B.CARD_RE[card_style].fullmatch(text)
                assert m and B.STYLE_OF_ADDRESS[m["address"]] == style and (m["auth"] == "Ana") == auth


def test_fixture_lexicon_forms_pass_their_unit_tests(ctx, plugin):
    reg = ctx.lexicon
    assert all(f.unit_ok for f in reg.forms.values()), {k: f.unit_problems for k, f in reg.forms.items()
                                                         if not f.unit_ok}
    assert reg.gate()["pass"]
    for sem in P.SIG:
        assert len(plugin._forms_of(sem)) >= 2, sem                # every sem has >= 2 usable forms
    for fid, f in reg.forms.items():
        if f.sem_id in P.SIG:
            assert P.lint_message_form(f.text) == [], f.text
            assert tuple(sorted(n for n, _ in f.slots)) == P.SIG[f.sem_id]


def test_message_lint_rejects_status_and_label_words():
    assert P.lint_message_form("All done, {TASK} is complete.")
    assert P.lint_message_form("I kept my word: {TASK}.")
    assert P.lint_message_form("Ask Dana about {TASK} by Monday.")
    assert P.lint_message_form("I'll {TASK} in 3 days.")
    assert P.lint_message_form("I'll {TASK} by tomorrow.")                   # v2: no date of its own (H9)
    assert P.lint_message_form("Give me two more weeks to {TASK}.")
    assert P.lint_message_form("Sounds good, thanks.") == []


# ------------------------------------------------------------------------------------------------ G2 / G3

def test_solver_a_equals_solver_b_on_5000_specs(plugin, ctx):
    seen = collections.Counter()
    for seed in range(1000):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            _check_row(plugin, ctx, spec, rr)
            seen[spec.qform] += 1
            for q2 in COMPLEMENT_FORMS.get(spec.qform, ()):
                s2 = spec.replace(qform=q2)
                r2 = plugin.render(s2, ctx, skin=ctx.skin(rr.skin_id), forms=rr.forms)
                _check_row(plugin, ctx, s2, r2)
                assert r2.answer == 1 - rr.answer
                seen[q2] += 1
    assert sum(seen[q] for q in ("ch_status", "ch_due") + YN_BASE) == 5000
    assert set(seen) == set(plugin.QFORMS) and min(seen.values()) > 120, seen


def test_every_unit_passes_the_program_gates(plugin, ctx):
    units, kinds = [], collections.Counter()
    for seed in range(150):
        for smp in SAMPLERS:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=(seed < 4))
            assert res.ok, (seed, smp, res.problems)
            units.append(res)
            for r in res.rows:
                kinds[(r["qtype"], r["role"])] += 1
                assert R.validate_row(r) == []
                if smp == "S5":
                    assert r["meta"]["dev_only"]
                else:
                    assert R.validate_row(r, training=True) == [] or r["meta"]["dev_only"]
    rep = pipeline.overlay_report(units, plugin)
    # 750 units: the shares of the 4 / 5 bands are checked tightly on 12,800 units in test_pilot_fixes.py (relations only)
    assert 0.40 <= rep["yes_no"] / rep["rows"] <= 0.60, rep
    assert rep["complement_share_of_yes_no"] >= 0.20 and rep["non_syntactic_share_of_pairs"] >= 0.30, rep
    assert 0.17 <= rep["twin_share"] <= 0.28, rep
    assert 0.03 <= rep["equiv_share"] <= 0.10 and 0.02 <= rep["attack_share"] <= 0.08, rep
    for role in ("complement", "twin", "equiv", "attack"):
        assert sum(v for (q, r), v in kinds.items() if r == role) > 10, (role, kinds)


# ------------------------------------------------------------------------------------------------ relations

def test_relations_are_valid(plugin, specs):
    twins, comps, meta = collections.Counter(), 0, 0
    for spec in specs:
        base = plugin.solve_a(spec)
        for prop in plugin.relations(spec):
            if prop.kind == "twin":
                twin = plugin.derive(prop.spec)
                assert slot_diff(spec, twin) == {prop.changed_slot}
                assert twin.structure == spec.structure and twin.qform == spec.qform
                got = plugin.solve_a(twin)
                assert got == prop.expect != base, (spec.seed, spec.sampler, prop.note)
                if spec.qform.startswith("yn_"):
                    assert got == 1 - base
                twins[prop.note.split(".")[-1]] += 1
            elif prop.kind == "complement":
                partner = spec.replace(qform=prop.qform)
                q, q2 = plugin.QFORMS[spec.qform], plugin.QFORMS[prop.qform]
                assert q.predicate == q2.predicate and q.polarity == -q2.polarity
                assert plugin.solve_a(partner) == 1 - base
                comps += 1
            elif prop.kind == "metamorphic":
                moved = plugin.derive(prop.spec)
                assert plugin.solve_a(moved) == (base if prop.expect == "same" else prop.expect), prop.note
                meta += 1
    assert {"asof", "done_date", "release_by", "yes_by", "auth", "cond_flip"} <= set(twins), twins
    assert sum(twins.values()) >= 0.3 * len(specs) and comps > 250 and meta >= 3 * len(specs) - 50


def test_twins_change_one_slot_in_the_rendered_text(plugin, ctx):
    """G-TW on the text: outside the changed slot the twin row is identical (checked by the kit emitter)."""
    checked = collections.Counter()
    for seed in range(150):
        spec = plugin.sample(seed, "S2")
        twin = next((p for p in plugin.relations(spec) if p.kind == "twin"), None)
        if twin is None:
            continue
        res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
        assert res.ok, res.problems
        rows = {r["role"]: r for r in res.rows}
        if "twin" in rows:
            assert rows["twin"]["meta"]["twin_of"] == rows["base"]["id"]
            assert rows["twin"]["call_id"] != rows["base"]["call_id"]
            assert rows["twin"]["gold"] != rows["base"]["gold"]
            checked[twin.note] += 1
    assert sum(checked.values()) > 40 and len(checked) >= 4, checked


# ------------------------------------------------------------------------------------------------ balance

def test_gold_balance_on_2000_specs(plugin, specs):
    yes = collections.defaultdict(list)
    status, due = collections.Counter(), collections.Counter()
    for spec in specs:
        gold = plugin.solve_a(spec)
        if spec.qform in YN_BASE:
            yes[spec.qform].append(gold)
        elif spec.qform == "ch_status":
            status[gold] += 1
        else:
            due["original" if gold == spec.slots["DUE0"].value.isoformat() else "extended"] += 1
    for q, golds in yes.items():                                  # exact by seed pairs (G0 section 4)
        assert abs(sum(golds) / len(golds) - 0.5) <= 0.03, (q, sum(golds), len(golds))
    n = sum(status.values())
    assert set(status) == set(P.STATUSES)
    for st in P.STATUSES:
        assert 0.12 <= status[st] / n <= 0.30, status
    assert 0.40 <= due["extended"] / sum(due.values()) <= 0.60, due
    assert sum(s.deep for s in specs) / len(specs) <= 0.10
    qf = collections.Counter(s.qform for s in specs)
    assert 0.40 <= sum(qf[q] for q in YN_BASE) / len(specs) <= 0.50, qf
    bad_yes = [plugin.solve_a(s) for s in specs if plugin.QFORMS[s.qform].yes_is_bad]
    good_yes = [plugin.solve_a(s) for s in specs if plugin.QFORMS[s.qform].yes_is_bad is False]
    assert bad_yes and good_yes


def test_trap_floors_on_2000_specs(specs):
    tags = collections.Counter(t for s in specs for t in s.tags)
    share = {k: v / len(specs) for k, v in tags.items()}
    floors = {"latest_misleads": 0.25, "boundary": 0.30, "conditional": 0.30, "extension": 0.25,
              "unallowed_move": 0.20, "try_decoy": 0.20, "after_asof": 0.12, "retract": 0.10, "late_done": 0.05,
              "auth_third": 0.04}
    for t, want in floors.items():
        assert share.get(t, 0) >= 0.8 * want, (t, share)


def test_status_is_not_predicted_by_chat_size(plugin, specs):
    """Label-blind display: the number of chat lines carries little information about the status (G6 proxy)."""
    by = collections.defaultdict(list)
    for s in specs:
        if s.qform == "ch_status":
            by[plugin.solve_a(s)].append(len(s.structure["msgs"]))
    means = {k: sum(v) / len(v) for k, v in by.items()}
    assert max(means.values()) - min(means.values()) <= 2.0, means


def test_options_come_from_named_error_models(plugin, ctx, specs):
    models = set(plugin.error_models())
    sets, named, closed_rows = [], 0, 0
    for spec in specs:
        if spec.qform not in ("ch_status", "ch_due"):
            continue
        rr = plugin.render(spec, ctx)
        os_ = rr.option_set
        sets.append(os_)
        for o in os_.options:
            if o.role == "error":
                assert o.err and set(o.err) <= models
            else:
                assert o.role == "gold" or (o.role == "closed" and spec.qform == "ch_status"), o
        if spec.qform == "ch_status":
            assert sorted(os_.texts) == sorted(P.STATUS_TEXT.values())
            closed_rows += 1
            named += any(o.role == "error" for o in os_.options)
        else:
            assert len(os_.options) == P.DUE_K == 3               # open set: every wrong date is a named model
            assert {m for o in os_.options for m in o.err} <= set(P.DUE_OPTION_MODELS)
    for k, c in position_counts(sets).items():
        m = sum(c) / k
        if m >= 50:
            assert all(abs(x - m) <= 0.35 * m for x in c), (k, c)
    assert named / closed_rows >= 0.85, (named, closed_rows)    # closed rows nearly always show a named error


def test_due_options_carry_no_rank_cue(plugin, ctx):
    """Review fix: ch_due was k = 4, else 3 (k lowered after a failed build), and the gold sat at the top sorted rank
    on 42% of k = 3 rows (chance 33%): extended golds always had the original date below them, and the neighbouring
    due date fell below more often. Now k = 3 on every row (gold, the other asked date, the neighbouring due date),
    the decoy due dates fall before / between / after the asked two dates 1/3 each by one label-blind draw, and over
    every emitted ch_due row each sorted rank is within 4 standard errors of 1/3 and the neighbour's place does not
    depend on the gold."""
    from c2_kit import distractors as DI
    ranks, where, n, drops = collections.Counter(), collections.Counter(), 0, 0
    sets = []
    for seed in range(2400):
        for smp in TRAINING:
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_due":
                continue
            try:
                os_ = plugin.render(spec, ctx).option_set
            except K.RenderError:
                drops += 1
                continue
            sets.append(os_)
            gold = os_.gold.key
            keys = sorted(o.key for o in os_.options)
            ranks[keys.index(gold)] += 1
            d0, d2 = spec.slots["DUE0"].value.isoformat(), spec.slots["NEWDUE0"].value.isoformat()
            nb = [o.key for o in os_.options if "t32_wrong_commitment" in o.err]
            assert len(nb) == 1 and nb[0] not in (d0, d2)
            ext = gold == d2
            assert gold in (d0, d2) and {o.key for o in os_.options} == {d0, d2, nb[0]}
            where[(ext, "before" if nb[0] < d0 else "after" if nb[0] > d2 else "between")] += 1
            n += 1
    assert drops == 0 and n >= 1000, (drops, n)
    tol = 4 * ((1 / 3) * (2 / 3) / n) ** 0.5
    assert max(abs(ranks[r] / n - 1 / 3) for r in range(3)) <= tol, (ranks, n)
    cues = DI.ordered_cues(sets)[3]
    assert max(cues["rank_rate"]) <= 1 / 3 + tol, cues
    for ext in (False, True):
        m = sum(v for (e, _w), v in where.items() if e == ext)
        assert max(abs(where[(ext, w)] / m - 1 / 3) for w in ("before", "between", "after")) <= 0.06, where


# ------------------------------------------------------------------------------------------------ length

def test_rows_fit_the_length_caps(plugin, ctx):
    sizes = []
    for seed in range(200):
        for smp in SAMPLERS:
            rr = plugin.render(plugin.sample(seed, smp), ctx)
            sizes.append(R.approx_tokens(rr.row))
    assert max(sizes) <= R.MAX_TOKENS


@pytest.mark.skipif(not TOKENIZER.is_file(), reason="local Qwen tokenizer file not cached")
def test_real_token_mean_is_at_most_800(plugin, ctx):
    from tokenizers import Tokenizer
    tok = Tokenizer.from_file(str(TOKENIZER))

    def n(t):
        return len(tok.encode(t or "", add_special_tokens=False).ids)

    sizes = []
    for seed in range(160):
        for smp in SAMPLERS:
            r = plugin.render(plugin.sample(seed, smp), ctx).row
            sizes.append(n(r["state"]) + n(r["card"]) + 2 * n(r["instructions"])
                         + sum(n(o) + 2 for o in (r["options"] or [])))
    assert sum(sizes) / len(sizes) <= 800 and max(sizes) <= 2000, (sum(sizes) / len(sizes), max(sizes))


# ------------------------------------------------------------------------------------------------ G-SL

def test_builtin_placeholder_skins_lint_clean(plugin, ctx):
    linted = 0
    for sk in ctx.skins.values():
        if sk.author_mode == "T":
            v = gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                                  name_allow=plugin.NAME_ALLOW)
            assert v == [], (sk.skin_id, v)
        else:
            assert gsl.lint_freeform(sk.text, dict(sk.brief), label_words=plugin.LABEL_WORDS) == []
        linted += 1
    assert linted == len(ctx.skins) >= 25
    label = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in plugin.LABEL_WORDS) + r")\b", re.I)
    for sk in ctx.skins.values():                                 # skins and attack notes carry no gold label
        if sk.kind in ("skin", "attack"):
            assert not label.search(sk.text), sk.skin_id


def test_no_literal_value_or_label_outside_slots(plugin, ctx):
    """Every number, date, name, task, event and message of a rendered row sits inside a slot span; the program chat
    block and the card carry no digit, month, weekday or name of their own; the chat block has no label word."""
    months = "|".join(S.MONTHS + S.MONTHS_ABBR + S.WEEKDAYS)
    label = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in plugin.LABEL_WORDS) + r")\b", re.I)
    for seed in range(150):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            names = {s.value for s in spec.all_slots().values() if s.kind == "name"}
            for fld in ("state", "instructions", "card"):
                text = rr.row[fld] or ""
                spans = sorted((sp.start, sp.end) for sp in rr.spans if sp.field == fld)
                rest, pos = [], 0
                for a, b in spans:
                    if a >= pos:
                        rest.append(text[pos:a])
                        pos = b
                rest.append(text[pos:])
                rest = "\x00".join(rest)
                assert not re.search(r"\d", rest), (seed, smp, fld)
                assert not re.search(rf"\b(?:{months})\b", rest), (seed, smp, fld)
                for v in names:
                    assert not re.search(r"(?<![\w-])" + re.escape(v) + r"(?![\w-])", rest), (v, seed, smp)
                if fld == "state":
                    assert not label.search(rest.split("Members:", 1)[-1]), (seed, smp)
            block = plugin.chat_template(spec)
            assert not re.search(r"\d", K.PH_RE.sub("", block)) and not label.search(K.PH_RE.sub("", block))
            for st in P.CARD_SHARES:
                card = plugin.card_template(spec, st)
                assert not re.search(r"\d", card) and not re.search(rf"\b(?:{months})\b", card)
            assert plugin.CLOSED_WORLD_SENTENCE in CD.split_rules(rr.row)[0]


# ------------------------------------------------------------------------------------------------ determinism

def test_sampling_and_rendering_are_deterministic(plugin, ctx):
    for seed in (0, 7, 31, 202):
        for smp in SAMPLERS:
            a, b = plugin.sample(seed, smp), plugin.sample(seed, smp)
            assert a.structure_hash() == b.structure_hash() and a.tags == b.tags
            assert plugin.render(a, ctx).row == plugin.render(b, ctx).row
    u1 = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    u2 = pipeline.build_unit(plugin, P.T32(lexicon=ctx.lexicon, vocab=PV.standin()).sample(17, "S4"), ctx,
                             run_g15=False).rows
    assert u1 == u2
    hashes = {plugin.sample(seed, "S1").structure_hash() for seed in range(200)}
    assert len(hashes) == 200


def test_nothing_is_written(plugin, ctx):
    here = Path(__file__).resolve().parent
    before = sorted(p.name for p in here.iterdir())
    pipeline.build_unit(plugin, plugin.sample(3, "S1"), ctx, run_g15=False)
    assert sorted(p.name for p in here.iterdir()) == before
    if not paths.a38_frozen():
        with pytest.raises(paths.DataBeforeFreeze):
            paths.write_jsonl(paths.C2_PARTS / "t32_never.jsonl", [])


# ------------------------------------------------------------------------------------------------ injected bugs

def _failures(plugin, ctx, n=40):
    out = collections.Counter()
    for seed in range(n):
        for smp in TRAINING:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            for g, _ in res.problems:
                out[g] += 1
    return out


def test_g2_catches_a_solver_b_status_date_bug(plugin, ctx, monkeypatch):
    real = B.solve_b                                              # B counts one day past the status date

    def late(view):
        nxt = (dt.date.fromisoformat(view["asof"]) + dt.timedelta(days=1)).isoformat()
        return real(dict(view, asof=nxt))

    monkeypatch.setattr(B, "solve_b", late)
    assert _failures(plugin, ctx)["G2"] > 0


def test_g2_catches_a_solver_a_endpoint_bug(plugin, ctx, monkeypatch):
    specs = [plugin.sample(seed, smp) for seed in range(100) for smp in TRAINING]
    specs = [s for s in specs if "boundary" in s.tags and s.qform != "ch_due"]
    real = P.T32._fold
    monkeypatch.setattr(P.T32, "_fold", lambda self, spec, **kw: real(self, spec, **{**kw, "f": frozenset({
        "exclusive"})}))                                          # A reads "by D" as before D
    g2 = sum(g == "G2" for s in specs for g, _ in pipeline.check_rendered(plugin, s, plugin.render(s, ctx), ctx,
                                                                          run_g15=False))
    assert g2 > 0
    with pytest.raises(KP.ContractError):                         # and the sampler's own check refuses it too
        for seed in range(400):
            plugin.sample(seed, "S2")


def test_g2_catches_a_mislabelled_option(plugin, ctx, monkeypatch):
    monkeypatch.setitem(B.OPTION_STATUS, "Kept", "broken")
    monkeypatch.setitem(B.OPTION_STATUS, "Broken", "kept")
    f = _failures(plugin, ctx, 30)
    assert f["G2"] > 0


def test_g3_catches_a_renderer_that_drops_the_mentions(plugin, ctx, monkeypatch):
    real = P.T32.chat_template
    monkeypatch.setattr(P.T32, "chat_template", lambda self, spec: re.sub(r"@\{A\d+\} ", "", real(self, spec)))
    f = _failures(plugin, ctx, 20)
    assert f["G3"] + f["G2"] > 0 and f["G3"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = P.pick_choice_twins                                    # choice twins (yes/no bases carry none since v3)

    def flipped(key, pool, qform, keep, p_second):
        out = []
        for kind, name, twin, pred, v in real(key, pool, qform, keep, p_second):
            if qform == "ch_status":
                pred = next(s for s in P.STATUSES if s != pred)
            out.append((kind, name, twin, pred, v))
        return out

    monkeypatch.setattr(P, "pick_choice_twins", flipped)
    assert _failures(plugin, ctx)["G-TW"] > 0


def test_gsl_catches_a_leaky_skin(plugin, ctx):
    leaky = dataclasses.replace(ctx.skin("SK-TEAM-1"), skin_id="SK-LEAK",
                                text=ctx.skin("SK-TEAM-1").text + " Everything in it was kept.")
    c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK": leaky})
    spec = plugin.sample(5, "S1")
    rr = plugin.render(spec, c2, skin=leaky)
    assert any(g == "G-SL" for g, _ in pipeline.check_rendered(plugin, spec, rr, c2, run_g15=False))
