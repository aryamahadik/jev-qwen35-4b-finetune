"""In-memory tests for families/T01/haiku_author.py (nothing is written; Haiku is never run).

  budget     <= 40 authoring chunks, <= 50 items each; the G0 v2 section 7 counts (packs 80 / 16 held out, skins 56 per
             training register and 28 per held-out register, Mode F 120, wordings 287, window 14 per sem, comparator
             12 per sem)
  leak       every task file names its exact answer file; label-blind task files (packs, skins, Mode F) hold no T01
             label word and no fixture question text; no item holds a forbidden key or a never-open path
  checks     validate_pack / check_skin / check_freeform / check_wording / check_lexicon accept good pieces and reject
             leaky ones (label words, date and day-type words, kind words, wrong negation, inclusive "more than")
  registry   loaded Haiku forms enter the T01 registry as pending forms that pass their unit tests; a window form
             admitted 3/3 drives the plugin with solver A == solver B
Run (from lean/):  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T01/test_haiku_author.py
"""
from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker  # noqa: E402
from c2_kit.paths import never_open  # noqa: E402
from families.T01 import fixtures as FX  # noqa: E402
from families.T01 import haiku_author as HA  # noqa: E402
from families.T01 import plugin as P  # noqa: E402


@pytest.fixture(scope="module")
def batches():
    return HA.build_batches()


def _pack():
    return {"people": ["Ilse Varga", "Tomas Ruud", "Amaia Etxeberria", "Kofi Asante", "Mina Park", "Rafael Duarte"],
            "topics": {"rolling": "seasonal stay tally", "anchor": "appeal deadline", "waiting": "hail damage claim",
                       "purchase": "kitchen supply order", "cash": "till ledger review", "notice": "permit reply"},
            "filing": {"action": "appeal", "event_a": "decision date", "event_b": "posting date"},
            "perils": ["hail damage", "theft", "frozen pipe damage"],
            "vendors": ["Larchmont Goods", "Pellow Stores", "Vintry Hall Supply"]}


# ------------------------------------------------------------------------------------------------ budget

def test_batches_within_budget_and_counts(batches):
    assert sum(len(b.chunks) for b, _ in batches.values()) <= 40
    assert all(len(c["items"]) <= chunker.MAX_ITEMS for b, _ in batches.values() for c in b.chunks)
    plans = {name: plan for name, (_, plan) in batches.items()}
    assert len(plans["packs"]) == 80 and sum(m["held_out"] for m in plans["packs"].values()) == 16
    regs = collections.Counter((m["register"], m["held_out"]) for m in plans["skins"].values())
    assert {r for r, _ in regs} == set(P.T01.REGISTERS)
    assert all(regs[(r, False)] == 56 for r in HA.TRAIN_REGISTERS)
    assert all(regs[(r, True)] == 28 for r in P.T01.HELD_OUT_REGISTERS)
    assert len(plans["freeform"]) == 120
    per = collections.Counter(m["qform"] for m in plans["wordings"].values())
    assert set(per) == set(P.T01.FROZEN_QFORMS) and sum(per.values()) == 287
    assert min(per.values()) >= 9 and all(per[q] == 14 for q in HA.CHOICE)
    win = collections.Counter(m["sem"] for m in plans["windows"].values())
    assert win == {"win.rolling_cap": 14, "win.later_anchor": 14, "win.wait_after": 14}
    assert collections.Counter(m["sem"] for m in plans["comparators"].values()) == {"cmp.gt": 12, "cmp.ge": 12}
    for m in plans["wordings"].values():                              # slots: PERSON, REF + the kind's own only
        assert set(m["slots"]) <= {"PERSON", "REF"} | {"rolling": {"REF_DATE"}, "anchor": {"ACTION"},
                                                       "waiting": {"PERIL"}, "cash": {"DAY"}}.get(m["kind"], set())


# ------------------------------------------------------------------------------------------------ leak

def test_task_files_name_their_answer_and_leak_nothing(batches):
    root = HA.ROOT
    for name, (b, _) in batches.items():
        blind = b.kind in ("author_skin", "author_freeform", "author_pack")
        for c in b.chunks:
            ans = str(root / b.answer_path(c["task_id"]))
            text = HA.task_file_text(b, c, ans)
            assert f"    {ans}\n" in text and ans.endswith(f"answers/{c['task_id']}.json")
            assert never_open(ans) is None and never_open(str(root / f"tasks/{c['task_id']}.md")) is None
            low = text.lower()
            for q in HA.QSTRINGS:
                assert q.lower() not in low, (name, q)
            if blind:
                for w in P.T01.LABEL_WORDS:
                    assert not re.search(r"(?<![a-z0-9])" + re.escape(w) + r"(?![a-z0-9])", low), (name, w)
            for it in c["items"]:
                assert not (set(it) & chunker.FORBIDDEN_KEYS)


# ------------------------------------------------------------------------------------------------ checks

def test_pack_validator():
    assert HA.validate_pack(_pack()) == []
    p = _pack()
    bad = {
        "five people": {**p, "people": p["people"][:5]},
        "label word": {**p, "topics": {**p["topics"], "notice": "late reply check"}},
        "event label": {**p, "filing": {**p["filing"], "event_b": "posting"}},
        "contained": {**p, "filing": {**p["filing"], "event_b": "first decision date"}},
        "name inside": {**p, "vendors": ["Mina Park Goods", "Pellow Stores", "Vintry Hall Supply"]},
        "digit": {**p, "perils": ["hail damage", "theft", "flood 2"]},
        "negation": {**p, "perils": ["hail damage", "theft", "unpaid damage"]},
        "vendor case": {**p, "vendors": ["larchmont goods", "Pellow Stores", "Vintry Hall Supply"]},
        "never-open letters": {**p, "people": ["Ilse Varga", "Tomas Ruud", "Amaia Etxeberria", "Kofi Asante",
                                               "Mina Park", "Jevon Duarte"]},
    }
    for why, x in bad.items():
        assert HA.validate_pack(x), why


META_SKIN = {"register": "memo", "escape": "text", "held_out": False}


def test_check_skin_accepts_neutral_and_rejects_leaky_skins():
    good = "Desk memo: {PERSON} passed file {REF} about {a|TOPIC} to the review team for a check."
    sk, v = HA.check_skin("t01a.skin.memo.000", good, META_SKIN, "T01-task", "0" * 64, set())
    assert v == [] and sk.register == "memo"
    js = '{"file": {REF}, "sent_by": {PERSON}, "subject": {TOPIC}, "channel": "intake"}'
    assert HA.check_skin("t01a.skin.json.000", js, {**META_SKIN, "register": "json", "escape": "json"}, "t", "0" * 64,
                         set())[1] == []
    leaky = {"label": "{PERSON} sent file {REF} about the {TOPIC}; it looks late.",
             "date word": "{PERSON} sent file {REF} about the {TOPIC} before the deadline.",
             "kind word": "{PERSON} sent the insurance file {REF} about the {TOPIC}.",
             "question": "Did {PERSON} send file {REF} about the {TOPIC}?",
             "article": "{PERSON} sent file {REF} about a {TOPIC}.",
             "missing slot": "{PERSON} sent the file about the {TOPIC}.",
             "number": "{PERSON} sent two files, {REF} about the {TOPIC}."}
    for why, text in leaky.items():
        assert HA.check_skin("t01a.skin.memo.001", text, META_SKIN, "t", "0" * 64, set())[1], why


def test_check_freeform_keeps_the_facts():
    facts = {"PERSON": "Ines Moreau", "REF": "STAY-4821", "TOPIC": "visa stay count"}
    meta = {"register": "email", "facts": facts}
    good = "Hello,\nInes Moreau here. I am passing file STAY-4821 about the visa stay count to the desk.\nThanks"
    sk, v = HA.check_freeform("t01a.free.email.000", good, meta, "t", "0" * 64, set())
    assert v == [] and sk.author_mode == "F"
    for text in ("Ines Moreau sent file STAY-4821 about a visa stay count.",          # TOPIC not after "the"
                 "Ines Moreau sent file STAY-4821 about the visa stay count before the deadline.",
                 "Ines Moreau did not send file STAY-4821 about the visa stay count.",
                 "Ines Moreau sent file STAY-4821 about the visa stay count and Ines Moreau waits."):
        assert HA.check_freeform("t01a.free.email.001", text, meta, "t", "0" * 64, set())[1], text


@pytest.mark.parametrize("q, kind, slots, good, bad", [
    ("yn_over", "rolling", ["PERSON", "REF_DATE"], "As of {REF_DATE}, is {PERSON} over the stay limit?",
     "Is {PERSON} not over the stay limit on {REF_DATE}?"),
    ("yn_not_over", "rolling", ["PERSON"], "Is it true that {PERSON} has not gone over the stay limit?",
     "Is {PERSON} within the stay limit?"),
    ("yn_fail_time", "anchor", ["PERSON", "ACTION"],
     "Under the filing rule, did {PERSON} fail to file the {ACTION} in time?",
     "Did {PERSON} file the {ACTION} after the deadline?"),
    ("yn_cash_without", "cash", ["DAY", "REF"], "Does the cash rule let ledger {REF} close {DAY} without a report?",
     "Can ledger {REF} close {DAY} with no cash report?"),
    ("ch_due", "addon", ["REF"], "Under the response rule, on which date is the reply to notice {REF} due?",
     "Which option gives the correct answer for notice {REF}?"),
    ("ch_days", "rolling", ["REF"], "How many days present fall inside the checked window for record {REF}?",
     "How many business days present fall inside the checked window for record {REF}?"),
    ("yn_covered", "waiting", ["PERIL", "REF"], "Under the cover rule, is this {PERIL} loss on policy {REF} covered?",
     "Is the {PERIL} loss under policy {REF} covered now?"),
])
def test_check_wording(q, kind, slots, good, bad):
    meta = {"qform": q, "kind": kind, "slots": slots}
    obj, v = HA.check_wording("t01a.wording.x", good, meta, "t", "0" * 64, set())
    assert v == [] and obj[0] == q
    assert HA.check_wording("t01a.wording.y", bad, meta, "t", "0" * 64, set())[1]
    assert HA.check_wording("t01a.wording.z", good.replace("?", "."), meta, "t", "0" * 64, set())[1]
    office = {"qform": "yn_over", "kind": "rolling", "slots": ["REF"]}
    assert HA.check_wording("w", "Does the office count record {REF} as over the stay limit?", office, "t", "0" * 64,
                            set())[1]


def test_check_lexicon_shapes():
    def ok(sem, kind, slots, text):
        return HA.check_lexicon("i", text, {"sem": sem, "kind": kind, "slots": slots}, "t", "0" * 64, set())[1] == []
    X = {"X": "cents"}
    assert ok("cmp.gt", "comparator", X, "more than {X}") and ok("cmp.gt", "comparator", X, "strictly greater than {X}")
    assert ok("cmp.ge", "comparator", X, "{X} or above") and ok("cmp.ge", "comparator", X, "at least {X}")
    assert not ok("cmp.gt", "comparator", X, "above {X}") and not ok("cmp.gt", "comparator", X, "in excess of {X}")
    assert not ok("cmp.gt", "comparator", X, "{X} or more") and not ok("cmp.ge", "comparator", X, "more than {X}")
    for sem, text, kinds in FX.WINDOW_FORMS:
        assert ok(sem, "window", kinds, text), text
    NM = {"N": "count", "M": "count"}
    assert not ok("win.rolling_cap", "window", NM, "fewer than {N} in any {M:adj} period")
    assert not ok("win.rolling_cap", "window", NM, "at most {N} in each calendar year of {M}")
    assert not ok("win.later_anchor", "window", {"N": "count"}, "within {N} after the earlier of these two dates")
    assert not ok("win.later_anchor", "window", {"N": "count"}, "within {N} of these two dates")
    assert not ok("win.wait_after", "window", {"W": "count"}, "a waiting period of {W} that starts on its start date")


# ------------------------------------------------------------------------------------------------ registry

def test_loaded_forms_enter_the_registry_pending_and_drive_the_plugin():
    forms = [("win.rolling_cap", "window", "at most {N} during any rolling {M:adj} stretch",
              {"N": "count", "M": "count"}, "T01-task-w", "a" * 64),
             ("cmp.ge", "comparator", "equal to or more than {X}", {"X": "cents"}, "T01-task-c", "b" * 64)]
    wordings = [("yn_over", "Going by the record, has {PERSON} gone over the stay limit?", {"PERSON": "name"},
                 "T01-task-q", "c" * 64)]
    reg = HA.lexicon_registry(wordings, forms)
    assert len(reg.forms) == 3 and all(f.unit_ok for f in reg.forms.values())
    assert {reg.status(f) for f in reg.forms} == {"pending"}
    win = next(f for f in reg.forms.values() if f.sem_id == "win.rolling_cap")
    for e in range(3):
        reg.record_extraction(win.form_id, f"haiku:read-{e}", "win.rolling_cap")
    assert reg.status(win.form_id) == "admitted"
    ctx = FX.ctx()                                                    # fixture context plus the admitted Haiku form
    for f in reg.forms.values():
        if f.form_id == win.form_id:
            ctx.lexicon.forms[f.form_id] = f
    plugin = P.T01(lexicon=ctx.lexicon)
    plugin._forms_by_sem = {"win.rolling_cap": [win.form_id]}
    spec = plugin.sample(4, "S1")
    rr = plugin.render(spec, ctx)
    assert "during any rolling" in rr.row["instructions"]
    assert plugin.solve_b(plugin.parse(rr.row, ctx)) == plugin.solve_a(spec) == rr.answer
