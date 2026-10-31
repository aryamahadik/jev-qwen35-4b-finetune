"""families/T23/test_plugin.py: in-memory tests for the T23 plugin (A37 f: nothing is written; no Haiku, no network).

  contract        validate_plugin(strict) == [], solver-B independence, G0-lite frozen and <= 200 lines
  hand cases      worked examples with golds computed by hand (task_ranking example, every window rule at its
                  boundary, each clause type firing / not firing, a keep-old target two versions back): solver A,
                  solver B on the rendered row and the construction table all give the hand gold
  G0 v4 card      the frozen card lines (G0 1.1 table: shown-when rules) equal both solvers' copies; yes/no rows carry
                  the rules in row.card, choice rows in the instructions; list / table end-date markers and solver
                  B's refusal of a contradicting marker; day-count labels name their pair; a distinct wrong version
                  always exists; foreign clauses fail their own applies-test; a firing clause's target governs with a
                  newer version in force on the decision date (ambiguity pass H6-H14, H26)
  G2 / G3         solver A == solver B and parse == canonical on 5,000 sampled specs (+ every complement form)
  pipeline        every kit program gate (G2, G3, G4, G-SL, G-LEX, G-TW, schema; G15 on a slice) on 750 units,
                  and the spec 4.1 overlay shares
  relations       twins differ in exactly one input slot and the gold moves as constructed; complements opposite;
                  G4 metamorphic predictions hold
  balance         gold labels inside the G0 section 4 bands on 2,000 specs; trap shares; gold positions
  G-SL            the built-in placeholder skins, wordings and attack lines lint clean; no literal value or
                  gold-label word outside the slots of any rendered row
  determinism     same seed -> same spec and rows
  injected bugs   G2, G3 and G-TW catch a broken solver B, solver A, renderer, option text and twin prediction
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T23
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

from c2_kit import cards as CK  # noqa: E402
from c2_kit import gsl, paths, pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from c2_kit.plugin import Spec  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T23 import fixtures as FX  # noqa: E402
from families.T23 import plugin as P  # noqa: E402
from families.T23 import solver_b as B  # noqa: E402

SAMPLERS = P.T23.SAMPLERS
TRAINING = tuple(s for s in SAMPLERS if s not in P.T23.HELD_OUT_SAMPLERS)
BASE_YN = ("yn_version", "yn_claim", "yn_outcome")
COMPLEMENT_FORMS = {"yn_version": ("yn_version_other", "yn_version_not"),
                    "yn_claim": ("yn_claim_contra", "yn_claim_not"),
                    "yn_outcome": ("yn_outcome_out", "yn_outcome_not")}
TOKENIZER = Path(os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/"
                                    "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json"))
D = dt.date


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T23(lexicon=ctx.lexicon)


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


# ------------------------------------------------------------------------------------------------ contract

def test_plugin_meets_the_strict_contract(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []
    assert plugin.PARADIGM_A == "rule_engine" and plugin.PARADIGM_B == "sql_sqlite"
    g0 = Path(plugin.G0_LITE)
    assert len(g0.read_text(encoding="utf-8").splitlines()) <= 200
    assert hashlib.sha256(g0.read_bytes()).hexdigest() == plugin.G0_SHA256


def test_solver_b_shares_no_code_with_solver_a():
    src = Path(B.__file__).read_text(encoding="utf-8")
    assert "families.T23.plugin" not in src and "c2_kit.rules" not in src and "glob_a" not in src
    assert "import sqlite3" in src and "julianday" in src                 # the other paradigm, really used
    for name in KP.B_FORBIDDEN_NAMES:
        assert not re.search(rf"\b{name}\b", src), name


def test_fixture_lexicon_forms_pass_their_unit_tests(ctx):
    reg = ctx.lexicon
    assert all(f.unit_ok for f in reg.forms.values()), {k: f.unit_problems for k, f in reg.forms.items()
                                                         if not f.unit_ok}
    assert reg.gate()["pass"]
    asked = collections.Counter(sk.qform for sk in ctx.skins.values() if sk.kind == "wording")
    assert set(asked) == set(P.QF)


# ------------------------------------------------------------------------------------------------ hand cases

def _hand(plugin, *, dom="refunds", style="list", window="excl", anchor="FILING_DATE", starts, terms, dates,
          clause=None, sunset=None, qform="ch_version", qty=None, pointer=None):
    """A spec built by hand (no sampler): golds below are computed by hand from the G0 semantics table."""
    pack = P.DOMAINS[dom]
    slots = {"DOC": S.name_slot(pack.doc), "TERM_LABEL": S.name_slot(pack.term), "QTY_LABEL": S.name_slot(pack.qty),
             "CUSTOMER": S.name_slot("Dana Okafor"), "ORG": S.name_slot("Redfern Bank"),
             "ITEM": S.name_slot(pack.items[0]), "CASE_ID": S.id_slot("CASE-1234")}
    for r, label, d in zip(P.ROLES, pack.labels, dates):
        slots[P.LABEL_SLOT[r]] = S.name_slot(label)
        slots[r] = S.date_slot(d)
    for k, (s, t) in enumerate(zip(starts, terms), start=1):
        slots[f"V{k}_ID"] = S.id_slot(f"v{k}")
        slots[f"V{k}_START"] = S.date_slot(s)
        slots[f"V{k}_TERM"] = P._term_slot(pack.tkind, t)
    if sunset is not None:
        slots["SUNSET"] = S.date_slot(sunset)
    if pack.pair is None:
        slots["QTY"] = P._term_slot(pack.tkind, qty)
    if clause is not None:
        ctype, on = clause
        clause = {"type": ctype, "kind": P.CLAUSE_KIND[ctype], "on": on,
                  "role": P.KEEP_ROLE.get(ctype, "DECISION_DATE")}
    structure = {"domain": dom, "style": style, "window": window, "anchor": anchor, "n": len(starts),
                 "tkind": pack.tkind, "qty": list(pack.pair) if pack.pair else None, "clause": clause,
                 **(pointer or {})}
    return plugin.derive(Spec("T23", "S1", 0, "T23:S1:c00", qform, slots, structure=structure, pack=f"t23:{dom}"))


def _all_three(plugin, ctx, spec):
    """Solver A, solver B on the rendered row, and the construction table, on one hand spec."""
    rr = plugin.render(spec, ctx)
    _check_row(plugin, ctx, spec, rr)
    assert plugin._answer_st(spec, plugin._status(spec)) == plugin.solve_a(spec)
    return plugin.solve_a(spec)


def test_hand_case_task_ranking_example(plugin, ctx):
    """task_ranking T23 example: v1 14-day refund window, v2 30 days from 1 March 2026, purchases before 1 March stay
    under v1 (grandfather on v2). Bought 20 February, refund requested 10 March: default (request date) is v2, the
    clause moves the case to v1; 18 days > 14, so the request is outside the window."""
    kw = dict(starts=[D(2025, 6, 1), D(2026, 3, 1)], terms=[14, 30],
              dates=[D(2026, 2, 20), D(2026, 2, 23), D(2026, 3, 10), D(2026, 3, 12)], clause=("grandfather", 2))
    assert _hand(plugin, **kw).env()["QTY"] == 18
    assert _all_three(plugin, ctx, _hand(plugin, **kw, qform="ch_version")) == "v1"
    assert _all_three(plugin, ctx, _hand(plugin, **kw, qform="ch_term")) == 14
    assert _all_three(plugin, ctx, _hand(plugin, **kw, qform="yn_outcome")) == 0
    assert _all_three(plugin, ctx, _hand(plugin, **kw, qform="yn_outcome_out")) == 1
    assert _all_three(plugin, ctx, _hand(plugin, **kw, qform="yn_claim", pointer={"claim": "V2_TERM"})) == 0
    assert _all_three(plugin, ctx, _hand(plugin, **kw, qform="yn_version", pointer={"candidate": "V1_ID"})) == 1
    spec = _hand(plugin, **kw, qform="ch_version")
    em = {m: plugin._resolve(spec, frozenset({m})) for m in P.VER_EM}
    assert em["newest_version"] == em["t23_ignore_clause"] == 2
    # read on the decision date the default is v2 again, and the grandfather clause still sends the case to v1
    assert em["t23_original_version"] == em["t23_purchase_date"] == em["t23_event_date"] == em["t23_decision_date"] == 1
    assert em["t23_filing_date"] is None                               # the anchor itself: no misreading


@pytest.mark.parametrize("style,window", [("list", "incl"), ("table", "incl"), ("list", "excl"), ("table", "excl"),
                                          ("log", "chain")])
def test_hand_case_window_boundaries(plugin, ctx, style, window):
    """v2 starts 1 July 2025. incl prints v1's end as 30 June (included); excl prints 1 July (excluded); the chain
    rule prints no end. On 30 June v1 is in force, on 1 July v2, under every rule."""
    for event, want in ((D(2025, 6, 30), "v1"), (D(2025, 7, 1), "v2")):
        spec = _hand(plugin, dom="warranties", style=style, window=window, anchor="EVENT_DATE",
                     starts=[D(2025, 1, 1), D(2025, 7, 1)], terms=[90, 365],
                     dates=[D(2025, 6, 1), event, D(2025, 7, 20), D(2025, 8, 1)])
        assert _all_three(plugin, ctx, spec) == want, (style, window, event)
    end = _hand(plugin, dom="warranties", style=style, window=window, anchor="EVENT_DATE",
                starts=[D(2025, 1, 1), D(2025, 7, 1)], terms=[90, 365],
                dates=[D(2025, 6, 1), D(2025, 6, 2), D(2025, 7, 20), D(2025, 8, 1)]).env().get("V1_END")
    assert end == {"incl": D(2025, 6, 30), "excl": D(2025, 7, 1), "chain": None}[window]


def test_hand_case_retroactive_clause(plugin, ctx):
    """retro on v3 (starts 1 March 2026): an older version would govern (the event is under v1) and the decision is
    on 1 March: v3 governs; decided 28 February: v1 stays. v2 is skipped over (older than v3 too). A case whose
    default is v3 itself is not touched."""
    base = dict(dom="fees", anchor="EVENT_DATE", starts=[D(2025, 1, 1), D(2025, 9, 1), D(2026, 3, 1)],
                terms=[1500, 2500, 4000], clause=("retroactive", 3), qty=2000)
    on = _hand(plugin, **base, dates=[D(2025, 2, 1), D(2025, 3, 1), D(2025, 4, 1), D(2026, 3, 1)])
    before = _hand(plugin, **base, dates=[D(2025, 2, 1), D(2025, 3, 1), D(2025, 4, 1), D(2026, 2, 28)])
    assert _all_three(plugin, ctx, on) == "v3" and _all_three(plugin, ctx, before) == "v1"
    assert "boundary" in plugin._tags(on, plugin._status(on))
    newer = _hand(plugin, **base, dates=[D(2026, 3, 2), D(2026, 3, 3), D(2026, 3, 4), D(2026, 3, 9)])
    assert _all_three(plugin, ctx, newer) == "v3"
    assert plugin._status(newer)["clause"]["applies"] is False
    out = _hand(plugin, **{**base, "qty": 2400}, dates=[D(2025, 2, 1), D(2025, 3, 1), D(2025, 4, 1), D(2026, 3, 1)],
                qform="yn_outcome")
    assert _all_three(plugin, ctx, out) == 1                    # $24.00 <= v3's $40.00 cap


def test_hand_case_sunset_clause(plugin, ctx):
    """sunset on v1 at 30 September 2025 (v2 from 1 July 2025): default v1 by the event date; decided on 30 September
    (not after): v1; decided 1 October: v2."""
    base = dict(dom="travel", style="log", window="chain", anchor="EVENT_DATE",
                starts=[D(2025, 1, 1), D(2025, 7, 1), D(2026, 1, 1)], terms=[15000, 20000, 25000],
                clause=("sunset", 1), sunset=D(2025, 9, 30), qty=18000)
    stay = _hand(plugin, **base, dates=[D(2025, 5, 1), D(2025, 6, 10), D(2025, 6, 20), D(2025, 9, 30)])
    move = _hand(plugin, **base, dates=[D(2025, 5, 1), D(2025, 6, 10), D(2025, 6, 20), D(2025, 10, 1)])
    assert _all_three(plugin, ctx, stay) == "v1" and _all_three(plugin, ctx, move) == "v2"
    yn = dict(base, qform="yn_outcome")
    assert _all_three(plugin, ctx, _hand(plugin, **yn, dates=[D(2025, 5, 1), D(2025, 6, 10), D(2025, 6, 20),
                                                               D(2025, 9, 30)])) == 0      # $180 > $150 (v1)
    assert _all_three(plugin, ctx, _hand(plugin, **yn, dates=[D(2025, 5, 1), D(2025, 6, 10), D(2025, 6, 20),
                                                               D(2025, 10, 1)])) == 1      # $180 <= $200 (v2)


def test_hand_case_keep_old_clauses(plugin, ctx):
    """prospective on v3 (role event): the filing date (anchor) is under v3 and the event is under v1, so the case
    goes to v1, two versions back (not merely the version v3 replaces). An event exactly on v3's start date is not
    before it: v3 stays. A grandfather clause on v2 is a distractor when the default is v3."""
    base = dict(dom="leave", style="table", window="incl", anchor="FILING_DATE",
                starts=[D(2024, 1, 1), D(2024, 7, 1), D(2025, 1, 1)], terms=[10, 15, 20], qty=12)
    back2 = _hand(plugin, **base, clause=("prospective", 3),
                  dates=[D(2024, 2, 1), D(2024, 3, 1), D(2025, 1, 10), D(2025, 1, 20)])
    on_start = _hand(plugin, **base, clause=("prospective", 3),
                     dates=[D(2024, 2, 1), D(2025, 1, 1), D(2025, 1, 10), D(2025, 1, 20)])
    foreign = _hand(plugin, **base, clause=("grandfather", 2),
                    dates=[D(2024, 2, 1), D(2024, 3, 1), D(2025, 1, 10), D(2025, 1, 20)])
    assert _all_three(plugin, ctx, back2) == "v1"
    assert _all_three(plugin, ctx, on_start) == "v3"
    assert _all_three(plugin, ctx, foreign) == "v3"
    assert plugin._resolve(foreign, frozenset({"t23_foreign_clause"})) == 1     # the distractor reading
    excl = _hand(plugin, **{**base, "window": "excl"}, clause=("prospective", 3),
                 dates=[D(2024, 2, 1), D(2025, 1, 1), D(2025, 1, 10), D(2025, 1, 20)])
    assert _all_three(plugin, ctx, excl) == "v3"
    # "before" read as "on or before", and the start date read as still under the old version: v2
    assert plugin._resolve(excl, frozenset({"add_exclusive_endpoint"})) == 2


def test_hand_case_clause_target_with_a_newer_version_in_force_on_the_decision_date(plugin, ctx):
    """G0 R7, R8 and the card's clause line (ambiguity pass H13): the version a firing clause points to governs even
    when a newer version is in force on the decision date. Retro on v2: the event is under v1 and the decision date
    falls under v3, so v2 governs; sunset on v1 (30 September 2025): decided under v3, v2 governs."""
    starts = [D(2025, 1, 1), D(2025, 7, 1), D(2026, 1, 1)]
    retro = _hand(plugin, dom="fees", anchor="EVENT_DATE", starts=starts, terms=[1500, 2500, 4000],
                  clause=("retroactive", 2), qty=2000,
                  dates=[D(2025, 2, 1), D(2025, 3, 1), D(2025, 4, 1), D(2026, 2, 1)])
    assert _all_three(plugin, ctx, retro) == "v2"
    assert plugin._resolve(retro, frozenset({"t23_decision_date"})) == 3          # reading "today" is the error
    sunset = _hand(plugin, dom="travel", style="log", window="chain", anchor="EVENT_DATE", starts=starts,
                   terms=[15000, 20000, 25000], clause=("sunset", 1), sunset=D(2025, 9, 30), qty=18000,
                   dates=[D(2025, 5, 1), D(2025, 6, 10), D(2025, 6, 20), D(2026, 2, 1)])
    assert _all_three(plugin, ctx, sunset) == "v2"


def test_resolved_card_and_record_text(plugin, ctx):
    """G0 v2 (ambiguity pass H6-H13, H8), kept in v4: a card with a clause defines "would govern" as the default and
    prints at most one clause that moves a case only by its own condition; the excl rule says "the day before its end
    date"; list and table heads mark every printed end date as included (incl) or excluded (excl), the change log
    prints none; a middle version prints "replaces PREV; in force from S to END"."""
    cards = {True: set(), False: set()}
    for seed in range(60):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            card = plugin.card_template(spec)
            cards[spec.structure["clause"] is not None].add(card)
            assert card.endswith(P.CLOSED_WORLD) and plugin.CLOSED_WORLD_SENTENCE == P.CLOSED_WORLD
            assert P.WINDOW_RULE[spec.structure["window"]] in card
            if spec.structure["clause"] is not None:
                assert '"would govern" in a clause means this default' in card
                assert "At most one clause is printed: when its own condition holds, the version it points to governs" in card
                assert "even if another version is in force on a later date" in card
            else:                           # no clause printed: no clause rule, no "would govern", no date words line
                assert "would govern" not in card and "At most one clause" not in card and "Before" not in card
    assert cards[True] and cards[False]
    assert "through the day before its end date" in P.WINDOW_RULE["excl"] and "up to" not in P.WINDOW_RULE["excl"]
    seen = collections.Counter()
    for seed in range(60):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            st = spec.structure
            head = plugin.versions_template(spec).split("\n")[0]
            if st["style"] == "log":
                assert head == "Change log of the {DOC}, newest entry first:"
            else:
                assert head.endswith(f"({P.END_MARK[st['window']]}):"), head
            if st["style"] == "list" and st["n"] >= 3:
                assert re.search(r"\n- \{V2_ID\}: replaces \{V1_ID\}; in force from \{V2_START\} to \{V2_END\}; ",
                                 plugin.versions_template(spec))
            seen[(st["style"], st["window"])] += 1
    assert set(seen) == {("list", "incl"), ("list", "excl"), ("table", "incl"), ("table", "excl"), ("log", "chain")}


def _g0_card_rows(g0: str) -> list:
    """[(line id, shown-when, text)] from the G0 1.1 table."""
    sec = g0[g0.index("### 1.1"):g0.index("### 1.2")]
    rows = []
    for ln in sec.split("\n"):
        cells = [c.strip() for c in ln.strip().strip("|").split(" | ")] if ln.startswith("| ") else []
        if len(cells) == 3 and cells[0] not in ("Line", "---"):
            rows.append(tuple(cells))
    return rows


def _g0_card(rows: list, *, clause: bool, outcome: bool, claim: bool, window: str) -> str:
    """The card the G0 table prescribes for a record (its {ANCHOR} left as a slot)."""
    shown = {"always": True, "no clause printed": not clause, "a clause is printed": clause,
             "outcome question (yn_outcome, _out, _not)": outcome, "claim question (yn_claim, _contra, _not)": claim}
    out = []
    for _id, when, text in rows:
        if shown[when]:
            out.append(text.replace("{WINDOW}", P.WINDOW_RULE[window]))
    return "\n".join(out)


def test_g0_card_text_matches_both_solvers(plugin):
    """The frozen G0 1.1 card table is exactly the text solver A renders and solver B full-matches, for every
    (clause printed, outcome question, claim question, window rule) combination."""
    g0 = Path(plugin.G0_LITE).read_text(encoding="utf-8")
    rows = _g0_card_rows(g0)
    assert [r[0] for r in rows] == ["title", "default", "default_clause", "window", "clause", "dates", "within", "claim",
                                    "closed"]
    sec = g0[g0.index("### 1.1"):g0.index("### 1.2")]
    win = " ".join(sec[sec.index("{WINDOW}: incl"):].split())
    m = re.search(r'incl "(.+?)" excl "(.+?)" chain "(.+?)"', win)
    assert m and (m[1], m[2], m[3]) == tuple(P.WINDOW_RULE[k] for k in ("incl", "excl", "chain"))
    assert P.WINDOW_RULE == B._WINDOWS
    # solver B's card builder against the G0 table (the anchor slot still named {ANCHOR})
    for clause in (True, False):
        for outcome, claim in ((False, False), (True, False), (False, True)):
            for window in ("incl", "excl", "chain"):
                want = _g0_card(rows, clause=clause, outcome=outcome, claim=claim, window=window)
                assert B._card_template(B._WINDOWS[window], clause, outcome, claim) == want
    # solver A's card_template over sampled specs: the same table with the anchor label slot filled in
    seen = set()
    for seed in range(40):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            q = spec.qform
            want = _g0_card(rows, clause=spec.structure["clause"] is not None, outcome=q in P.OUTCOME_FORMS,
                            claim=q in P.CLAIM_FORMS, window=spec.structure["window"])
            want = want.replace("{ANCHOR}", "{" + P.LABEL_SLOT[spec.structure["anchor"]] + "}")
            assert plugin.card_template(spec) == want
            seen.add((spec.structure["clause"] is not None, q in P.OUTCOME_FORMS, q in P.CLAIM_FORMS))
    assert len(seen) == 6, seen
    for mark in P.END_MARK.values():
        assert f"({mark}):" in g0 and mark.split()[-1] == B.END_WORD[next(k for k, v in P.END_MARK.items()
                                                                          if v == mark)]


def test_v4_card_lines_are_the_v3_lines(plugin):
    """The v4 card changes no ruling (PILOT_VERDICT FIX-4 "without changing any H7 / H10-H13 ruling"): every sentence
    of the v3 card (G0_SPEC_v3.md, sha pinned in plugin.G0_SHA256_V3) is a v4 line word for word; v4 only leaves out
    the lines a row cannot use and rewrites the no-clause default line."""
    v3 = (Path(plugin.G0_LITE).parent / "G0_SPEC_v3.md").read_text(encoding="utf-8")
    assert hashlib.sha256(v3.encode("utf-8")).hexdigest() == plugin.G0_SHA256_V3
    sec = v3[v3.index("### 1.1"):v3.index("### 1.2")]
    v3_lines = [ln[4:] for ln in sec.split("\n") if ln.startswith("    ")]
    assert len(v3_lines) == 8
    items = {it.item_id: it.full for it in P.CARD_SPEC.items}
    assert "- " + items["default_clause"] == v3_lines[1]
    assert "- " + items["clause"] == v3_lines[3] and "- " + items["dates"] == v3_lines[4]
    assert "- " + items["within"] == v3_lines[5] and "- " + items["claim"] == v3_lines[6]
    assert P.CLOSED_WORLD == v3_lines[7]
    # the sentence the v3 card printed on every row, kept on every v4 row that needs it, and a marker guard for the
    # one rewritten line: the no-clause default keeps the anchor slot and drops only the clause reference
    assert not CK.variant_problems(items["default_clause"], items["default_clause"])
    assert "{ANCHOR}" in items["default"] and "clause" not in items["default"]
    assert P.CARD_SPEC.problems() == []


def test_solver_b_refuses_a_marker_that_contradicts_the_card(plugin, ctx):
    checked = 0
    for seed in range(40):
        spec = plugin.sample(seed, "S1")
        rr = plugin.render(spec, ctx)
        mark = P.END_MARK[spec.structure["window"]]
        other = next(v for v in P.END_MARK.values() if v != mark)
        assert f"({mark}):" in rr.row["state"]
        bad = dict(rr.row, state=rr.row["state"].replace(f"({mark}):", f"({other}):"))
        with pytest.raises(B.ParseError):
            B.parse(bad, ctx)
        checked += 1
    assert checked == 40


def test_day_count_labels_name_their_pair():
    """G0 section 7: a printed day count's label is "day count from A to B", A and B the pair's date labels without
    " date"; solver B reads the pair from the label alone (so Haiku packs need no solver-B table)."""
    for name, pack in P.DOMAINS.items():
        labels = list(pack.labels)
        got = B._day_pair(pack.qty, labels)
        if pack.pair is None:
            assert got is None and not pack.qty.startswith("day count"), name
            continue
        a, b = (P.ROLES.index(r) for r in pack.pair)
        assert pack.qty == f"day count from {labels[a][:-5]} to {labels[b][:-5]}", name
        assert got == (a, b), name
    labels = ["purchase date", "delivery date", "refund request date", "decision date"]
    with pytest.raises(B.ParseError):
        B._day_pair("day count from refund request to purchase", labels)          # later date first
    with pytest.raises(B.ParseError):
        B._day_pair("day count from purchase to repair", labels)                  # not a case date


def test_every_spec_has_a_distinct_wrong_version(plugin, specs):
    """G0 R14, section 5 (H26, H29): with n >= 2, newest_version and t23_original_version cannot both return the
    governing version, so a ch row always gets K = 2 options and a yn 'no' row always has a CANDIDATE / CLAIM."""
    for spec in specs:
        g = plugin._resolve(spec)
        wrong = {plugin._resolve(spec, frozenset({m})) for m in ("newest_version", "t23_original_version")}
        assert wrong - {g, None}, (spec.seed, spec.sampler)


def test_foreign_clauses_fail_their_own_applies_test(plugin, specs):
    """G0 section 3 (H14): foreign = the clause's own applies-test fails. keep-old / sunset: printed on c != D0;
    retroactive: D0 is V_c or newer (a retro clause on a version newer than D0 applies, so it is never foreign)."""
    seen = collections.Counter()
    for spec in specs:
        if "foreign_clause" not in spec.tags:
            continue
        cl, d0 = spec.structure["clause"], plugin._status(spec)["d0"]
        if cl["kind"] == "retro":
            assert d0 >= cl["on"], spec.seed
        else:
            assert d0 != cl["on"], spec.seed
        seen[cl["kind"]] += 1
    assert set(seen) == {"keep_old", "retro", "sunset"}


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
    assert sum(seen[q] for q in ("ch_version", "ch_term") + BASE_YN) == 5000
    assert set(seen) == set(plugin.QFORMS) and min(seen.values()) > 500, seen


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
    assert 0.45 <= rep["yes_no"] / rep["rows"] <= 0.55, rep
    assert rep["complement_share_of_yes_no"] >= 0.20 and rep["non_syntactic_share_of_pairs"] >= 0.30, rep
    assert 0.20 <= rep["twin_share"] <= 0.25, rep
    assert 0.05 <= rep["equiv_share"] <= 0.10 and 0.01 <= rep["attack_share"] <= 0.06, rep
    assert 0.45 <= rep["yes_rate"] <= 0.55, rep
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
                assert plugin._valid(twin)
                got = plugin.solve_a(twin)
                assert got == prop.expect != base, (spec.seed, spec.sampler, prop.note)
                twins[prop.note] += 1
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
    # every twin kind of G0 section 6 occurs: the default version, the clause state, Q and the governing term
    assert {"d0", "clause", "q", "terms"} <= set(twins), twins
    assert comps > 300 and meta >= 4 * len(specs)


def test_twins_change_one_slot_in_the_rendered_text(plugin, ctx):
    """G-TW on the text: outside the changed slot (and the derived ends / day count it feeds) the twin row is
    identical, and the twin keeps its own call_id."""
    checked = 0
    for seed in range(150):
        spec = plugin.sample(seed, "S2")
        if not any(p.kind == "twin" for p in plugin.relations(spec)):
            continue
        res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
        assert res.ok, res.problems
        rows = {r["role"]: r for r in res.rows}
        if "twin" in rows:
            assert rows["twin"]["meta"]["twin_of"] == rows["base"]["id"]
            assert rows["twin"]["call_id"] != rows["base"]["call_id"]
            checked += 1
    assert checked > 40


# ------------------------------------------------------------------------------------------------ balance

def test_gold_balance_on_2000_specs(plugin, specs):
    yes = collections.defaultdict(list)
    newest = collections.Counter()
    for spec in specs:
        gold = plugin.solve_a(spec)
        if spec.qform in BASE_YN:
            yes[spec.qform].append(gold)
        newest[plugin._resolve(spec) == spec.structure["n"]] += 1
    for q, golds in yes.items():                                  # exact by seed pairs (G0 section 4)
        assert abs(sum(golds) / len(golds) - 0.5) <= 0.03, (q, sum(golds), len(golds))
    assert 0.35 <= newest[True] / len(specs) <= 0.65, newest      # no strong newest / not-newest prior
    assert sum(s.deep for s in specs) / len(specs) <= 0.10
    qf = collections.Counter(s.qform for s in specs)
    assert 0.38 <= sum(qf[q] for q in BASE_YN) / len(specs) <= 0.50, qf
    scen = collections.Counter(next((t for t in s.tags if t in ("plain", "clause_decisive", "clause_tested",
                                                                 "foreign_clause"))) for s in specs)
    assert scen["plain"] / len(specs) <= 0.30, scen


def test_trap_shares_on_2000_specs(plugin, specs):
    tags = collections.Counter(t for s in specs for t in s.tags)
    share = {k: v / len(specs) for k, v in tags.items()}
    targets = {"newest_wrong": 0.30, "foreign_clause": 0.30, "clause_decisive": 0.25, "boundary": 0.20}
    for t, want in targets.items():
        assert share.get(t, 0) >= 0.9 * want, (t, share)
    for t in ("clause_tested", "term_edge", "future_version", "grandfather", "prospective", "retroactive", "sunset"):
        assert share.get(t, 0) > 0.01, (t, share)
    # every clause type fires on some rows, is tested without firing on others, and sits as a distractor on others
    seen = {(t, o) for s in specs for t in s.tags for o in s.tags
            if t in ("grandfather", "prospective", "retroactive", "sunset")
            and o in ("clause_decisive", "clause_tested", "foreign_clause")}
    for t in ("grandfather", "prospective", "retroactive", "sunset"):
        for o in ("clause_decisive", "clause_tested", "foreign_clause"):
            assert (t, o) in seen, (t, o)


def test_options_come_from_named_error_models(plugin, ctx, specs):
    positions = collections.defaultdict(collections.Counter)
    used = collections.Counter()
    for spec in specs:
        if spec.qform not in ("ch_version", "ch_term"):
            continue
        rr = plugin.render(spec, ctx)
        os_ = rr.option_set
        positions[len(os_.options)][os_.gold_index] += 1
        for o in os_.options:
            if o.role == "error":
                assert o.err and set(o.err) <= set(P.VER_EM)
                used.update(o.err)
            else:
                assert o.role == "gold"
    for k, c in positions.items():
        m = sum(c.values()) / k
        if m >= 50:
            assert all(abs(c[i] - m) <= 0.35 * m for i in range(k)), (k, c)
    assert set(used) == set(P.VER_EM), used                       # every named model produces some option


def test_choice_options_carry_no_sort_cue(plugin, ctx):
    """Review fix: ch_version / ch_term drew k = 2-4 and lowered k after a failed build, and with v1 / rev-A ids the
    gold was the higher-sorting id on 62% of k = 2 rows. Now k = 2 on every row (never lowered), ch_version ids are
    random codes, and over every emitted row the gold is the higher-sorting option within 4 standard errors of 1/2
    (ids for ch_version, values for ch_term)."""
    from c2_kit import distractors as DI
    hi, n, drops = collections.Counter(), collections.Counter(), 0
    for seed in range(2000):
        for smp in TRAINING:
            spec = plugin.sample(seed, smp)
            if spec.qform not in ("ch_version", "ch_term"):
                continue
            try:
                os_ = plugin.render(spec, ctx).option_set
            except K.RenderError:
                drops += 1
                continue
            assert len(os_.options) == P.CHOICE_K == 2
            if spec.qform == "ch_version":
                ids = [spec.slots[f"V{k}_ID"].value for k in range(1, spec.structure["n"] + 1)]
                assert not any(re.fullmatch(r"v\d|rev-[A-D]", x) for x in ids), ids
            cues = DI.ordered_cues([os_])[2]
            hi[spec.qform] += cues["rank_hits"][1]
            n[spec.qform] += 1
    assert drops == 0
    for q in ("ch_version", "ch_term"):
        assert n[q] >= 1000, n
        assert abs(hi[q] / n[q] - 0.5) <= 4 * (0.25 / n[q]) ** 0.5, (q, hi[q], n[q])


def test_yes_no_distractor_values_are_misreadings(plugin, specs):
    """A 'no' yn_version / yn_claim row names the version (term) some error model picks, never an arbitrary one."""
    checked = 0
    for spec in specs:
        if spec.qform not in ("yn_version", "yn_claim") or plugin.solve_a(spec) == 1:
            continue
        ptr = spec.structure.get("candidate") or spec.structure.get("claim")
        k = int(ptr[1:].split("_")[0])
        assert any(plugin._resolve(spec, frozenset({m})) == k for m in P.VER_EM)
        checked += 1
    assert checked > 100


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
    for seed in range(120):
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
    assert linted == len(ctx.skins) >= 29
    for sk in ctx.skins.values():                                 # skins and attack lines carry no gold label
        if sk.kind in ("skin", "attack"):
            low = sk.text.lower()
            assert not any(w in low for w in plugin.LABEL_WORDS), sk.skin_id


def test_no_literal_value_or_label_outside_slots(plugin, ctx):
    """Every number, date, amount, name and id of a rendered row sits inside a slot span; program templates and the
    card carry no digit, month or weekday of their own, and the record blocks no gold-label word."""
    months = "|".join(S.MONTHS + S.WEEKDAYS)
    label = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in plugin.LABEL_WORDS) + r")\b", re.I)
    for seed in range(150):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            values = {str(s.value) for s in spec.all_slots().values() if s.kind in ("name", "id")}
            for fld in ("state", "card", "instructions"):
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
                for v in values:
                    assert not re.search(r"(?<![\w-])" + re.escape(v) + r"(?![\w-])", rest), (v, seed, smp)
            clause = plugin.clause_template(spec)
            for tpl in (plugin.versions_template(spec), plugin.case_template(spec)):
                assert not re.search(r"\d", K.PH_RE.sub("", tpl))
                # the clause line is a conditional rule ("... X governs it instead"); every other line is a record
                assert not label.search(tpl.replace(clause, "") if clause else tpl), tpl
            card = plugin.card_template(spec)
            assert not re.search(r"\d", K.PH_RE.sub("", card)) and not re.search(rf"\b(?:{months})\b", card)


# ------------------------------------------------------------------------------------------------ determinism

def test_sampling_and_rendering_are_deterministic(plugin, ctx):
    for seed in (0, 7, 31, 202):
        for smp in SAMPLERS:
            a, b = plugin.sample(seed, smp), plugin.sample(seed, smp)
            assert a.structure_hash() == b.structure_hash() and a.tags == b.tags
            assert plugin.render(a, ctx).row == plugin.render(b, ctx).row
    u1 = pipeline.build_unit(plugin, plugin.sample(17, "S4"), ctx, run_g15=False).rows
    u2 = pipeline.build_unit(plugin, P.T23(lexicon=ctx.lexicon).sample(17, "S4"), ctx, run_g15=False).rows
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
            paths.write_jsonl(paths.C2_PARTS / "t23_never.jsonl", [])


# ------------------------------------------------------------------------------------------------ injected bugs

def _failures(plugin, ctx, n=40):
    out = collections.Counter()
    for seed in range(n):
        for smp in TRAINING:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            for g, _ in res.problems:
                out[g] += 1
    return out


def test_g2_catches_a_solver_b_window_end_bug(plugin, ctx, monkeypatch):
    real = B._in_force                                             # B reads every inclusive end as exclusive
    monkeypatch.setattr(B, "_in_force", lambda db, role, window: real(db, role, "excl" if window == "incl" else window))
    assert _failures(plugin, ctx, 80)["G2"] > 0


def test_g2_catches_a_solver_b_clause_bug(plugin, ctx, monkeypatch):
    real = B._governing                                            # B ignores every clause

    def no_clause(db, view):
        return real(db, dict(view, clause=None))

    monkeypatch.setattr(B, "_governing", no_clause)
    assert _failures(plugin, ctx)["G2"] > 0


def test_g2_catches_a_solver_a_boundary_bug(plugin, ctx, monkeypatch):
    specs = [plugin.sample(seed, smp) for seed in range(200) for smp in TRAINING]
    specs = [s for s in specs if "boundary" in s.tags and s.structure["window"] == "incl"]
    real = P.T23._window

    def strict(self, spec, k, d):                                  # solver A reads "through its end date" as strict
        node = real(self, spec, k, d)
        if isinstance(node, P.RL.And) and node.args[1].op == "<=":
            return P.RL.And((node.args[0], P.RL.Cmp("<", node.args[1].left, node.args[1].right)))
        return node

    rendered = [(s, plugin.render(s, ctx)) for s in specs]
    monkeypatch.setattr(P.T23, "_window", strict)
    g2 = 0
    for s, rr in rendered:
        try:
            probs = pipeline.check_rendered(plugin, s, rr, ctx, run_g15=False)
        except KP.ContractError:
            g2 += 1                                                # solver A finds no version: a G2 stop too
            continue
        g2 += sum(g == "G2" for g, _ in probs)
    assert g2 > 0
    with pytest.raises(KP.ContractError):                          # and the sampler's own guard refuses it
        for seed in range(400):
            plugin.sample(seed, "S2")


def test_g2_catches_a_mislabelled_option(plugin, ctx, monkeypatch):
    real = P.T23._term_text

    def off_by_one(self, spec):
        text = real(self, spec)
        return lambda x: text(x + 1)

    monkeypatch.setattr(P.T23, "_term_text", off_by_one)
    f = _failures(plugin, ctx, 60)
    assert f["G2"] + f["G3"] > 0


def test_g3_catches_a_renderer_that_drops_the_clause(plugin, ctx, monkeypatch):
    real = P.T23.versions_template

    def dropped(self, spec):
        return "\n".join(ln for ln in real(self, spec).split("\n") if "clause of" not in ln)

    monkeypatch.setattr(P.T23, "versions_template", dropped)
    assert _failures(plugin, ctx)["G3"] > 0


def test_g3_catches_a_renderer_that_misprints_an_end_date(plugin, ctx, monkeypatch):
    monkeypatch.setitem(P.WINDOW_RULE, "incl", P.WINDOW_RULE["excl"])  # incl ends printed under the excl rule
    assert _failures(plugin, ctx)["G3"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = P.T23._twin

    def flipped(self, spec):
        t = real(self, spec)
        if t is None or spec.qform in ("ch_version", "ch_term"):
            return t
        return dataclasses.replace(t, expect=1 - t.expect)

    monkeypatch.setattr(P.T23, "_twin", flipped)
    assert _failures(plugin, ctx)["G-TW"] > 0


def test_gsl_catches_a_leaky_skin(plugin, ctx):
    leaky = dataclasses.replace(ctx.skin("SK-CHAT-1"), skin_id="SK-LEAK",
                                text=ctx.skin("SK-CHAT-1").text + " The newest version governs it.")
    c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK": leaky})
    spec = plugin.sample(5, "S1")
    rr = plugin.render(spec, c2, skin=leaky)
    assert any(g == "G-SL" for g, _ in pipeline.check_rendered(plugin, spec, rr, c2, run_g15=False))
