"""t37b/test_t37b.py: in-memory tests for the T37b builder (A37 f: nothing is written; no replay row is read; no Haiku).

  registry      internal consistency; every registered source is KEEP in the real replay register (read with ast);
                excluded sources are never registered
  G0            the one-page spec is frozen and <= 200 lines
  independence  polarity_b.py imports neither negcount nor polarity.py (and the reverse)
  polarity      hand cases (right and wrong partners of every kind) read the same by programs A and B; mutation
                sweeps: no mutated partner passes both programs; exactly one "fail to" position passes
  selection     every spec 3.18 base rule drops what it should, with its counted reason; old slice by id, group, state
  plan          label-blind (flipping every gold leaves the plan unchanged); quotas, source and template caps on a
                larger stand-in pool; the complement count is cut to keep the floors
  rows          the full in-memory flow (stand-in admitted pool, program-written partners, finalize): gold relation,
                swapped / own / kept cards, relation edges, schema, G15 loader_check on every partner
  decision      keep / drop / review branches; Haiku items carry no gold, state or card where they must not;
                polarity items are one per distinct question pair; trim_block keeps the floors and caps
  writer        refuses before A38 and on a G0 problem; T37b-dev rows are dev-only and refused by
                validate_row(training=True)
  (author_pool.py has its own tests in test_author_pool.py)
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/t37b
"""
from __future__ import annotations

import ast
import inspect
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker, paths  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from t37b import author_pool as AP  # noqa: E402
from t37b import builder as BL  # noqa: E402
from t37b import fixtures as FX  # noqa: E402
from t37b import polarity as PA  # noqa: E402
from t37b import polarity_b as PB  # noqa: E402
from t37b import select as SEL  # noqa: E402
from t37b import sources as SRC  # noqa: E402

import negcount  # noqa: E402  (on sys.path through c2_kit.paths)

E = SRC.ENTRY_BY_KEY
TRAIN = SRC.FRAMES_TRAIN


CUST = SRC.Entry("gd_test", "t", r"[^?]+\?", ("syntactic", "implicit", "equiv"), subject="the customer", verb="get")
REPLY = SRC.Entry("gd_test", "r", r"[^?]+\?", ("syntactic", "implicit", "equiv"), subject="the reply", verb="contain")
REPLY_SHOW = SRC.Entry("gd_test", "s", r"[^?]+\?", ("syntactic", "implicit", "equiv"), subject="the reply", verb="show")
CAPS_HAVE = SRC.Entry("gd_test", "c", r"[^?]+\?", ("syntactic", "implicit", "equiv"),
                      subject=r"Ana Ruiz and Tomas Feld", verb="have")


def both(base, partner, kind, entry_key, frames=TRAIN):
    e = entry_key if isinstance(entry_key, SRC.Entry) else E[entry_key]
    return PA.classify_a(base, partner, kind, e, frames)[0], PB.classify_b(base, partner, kind, e, frames)[0]


# ------------------------------------------------------------------------------------------------ registry and G0

def test_registry_is_consistent():
    assert SRC.check_registry() == []
    assert not set(SRC.SOURCES) & set(SRC.EXCLUDED)


def test_registered_sources_are_keep_in_the_replay_register():
    keep = SEL.default_status()
    assert [s for s in SRC.SOURCES if not keep(s)] == []


def test_excluded_sources_never_select():
    for s in SRC.EXCLUDED:
        assert SRC.exclusion_reason(s)
    for s in ("gd_gen_tables", "pg_policy", "hard_nli_a", "binj_adult", "proc_trap", "gd_prontoqa", "gd_unknown_x"):
        assert SRC.exclusion_reason(s)


def test_g0_lite_frozen():
    assert BL.g0_problems() == []


def test_g0_resolves_every_point_of_the_haiku_pass():
    import hashlib
    import json
    rec = json.loads(BL.G0_HAIKU_POINTS.read_text(encoding="utf-8"))
    pts = rec["points"]
    assert rec["pass"] == BL.G0_HAIKU_TASK and rec["n_points"] == len(pts) == 61
    blob = json.dumps(pts, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    assert hashlib.sha256(blob.encode()).hexdigest() == rec["points_sha256"]
    text = BL.G0_LITE.read_text(encoding="utf-8")
    assert BL.G0_HAIKU_TASK in text and all(f"- H{n}: " in text for n in range(1, len(pts) + 1))
    assert f"- H{len(pts) + 1}: " not in text


def test_frames_hold_no_negation_cue():
    for f in SRC.FRAMES_TRAIN + SRC.FRAMES_DEV:
        assert negcount.count(f).k_all == 0
        assert not set(PB.tokens(f)) & PB.NEG_B


# ------------------------------------------------------------------------------------------------ independence

def _imports(mod) -> set:
    tree = ast.parse(inspect.getsource(mod))
    out = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            out |= {a.name for a in n.names}
        elif isinstance(n, ast.ImportFrom):
            out.add(n.module or "")
            out |= {f"{n.module}.{a.name}" for a in n.names}
    return out


def test_program_b_shares_no_code_with_program_a():
    imp_b = _imports(PB)
    assert not any("negcount" in m or "polarity" in m for m in imp_b), imp_b
    assert not any("polarity_b" in m for m in _imports(PA))


# ------------------------------------------------------------------------------------------------ polarity: hand cases

CV = "Does the evidence support the claim?"
HOT = "gd_hotpotqa_yesno/q"
HAND = [
    # (name, base, partner, kind, entry, expected relation from both programs)
    ("syn ok", CV, "Is it true that the evidence does not support the claim?", "syntactic", "gd_check_covid/support",
     "opposite"),
    ("syn n't", "Is this post hateful?", "Is it correct that this post isn't hateful?", "syntactic",
     "gd_hatemoji_build_v14/hateful", "opposite"),
    ("syn cannot", "Can the customer get a refund?", "Is it true that the customer cannot get a refund?", "syntactic",
     CUST, "opposite"),
    ("syn can't", "Can the customer get a refund?", "Is it true that the customer can't get a refund?", "syntactic",
     CUST, "opposite"),
    ("syn can not", "Can the customer get a refund?", "Is it true that the customer can not get a refund?",
     "syntactic", CUST, "opposite"),
    ("syn aux after the verb", "Can the customer get a refund?", "Is it true that the customer get cannot a refund?",
     "syntactic", CUST, None),
    ("syn not both", "Were Ana Ruiz and Tomas Feld both born in Portugal?",
     "Is it true that Ana Ruiz and Tomas Feld were not both born in Portugal?", "syntactic", HOT, "opposite"),
    ("syn both ... not (neither)", "Were Ana Ruiz and Tomas Feld both born in Portugal?",
     "Is it true that both Ana Ruiz and Tomas Feld were not born in Portugal?", "syntactic", HOT, None),
    ("syn matrix negation", CV, "Doesn't the evidence support the claim?", "syntactic", "gd_check_covid/support", None),
    ("syn two cues", CV, "Is it true that the evidence does not not support the claim?", "syntactic",
     "gd_check_covid/support", None),
    ("syn modal must", "Must the agent refund the order?", "Is it true that the agent must not refund the order?",
     "syntactic", HOT, None),
    ("syn unknown frame", CV, "Do you think that the evidence does not support the claim?", "syntactic",
     "gd_check_covid/support", None),
    ("syn dev frame in training", CV, "Is it so that the evidence does not support the claim?", "syntactic",
     "gd_check_covid/support", None),
    ("syn changed word", CV, "Is it true that the evidence does not support the new claim?", "syntactic",
     "gd_check_covid/support", None),
    ("syn not misplaced", CV, "Is it true that the evidence support does not the claim?", "syntactic",
     "gd_check_covid/support", None),
    ("syn never", CV, "Is it true that the evidence does never support the claim?", "syntactic",
     "gd_check_covid/support", None),
    ("syn quantifier subject", "Did all customers receive refunds?",
     "Is it true that all customers did not receive refunds?", "syntactic", HOT, None),
    ("imp ok", CV, "Does the evidence fail to support the claim?", "implicit", "gd_check_covid/support", "opposite"),
    ("imp quantifier", "Did all customers receive refunds?", "Did all customers fail to receive refunds?", "implicit",
     HOT, None),
    ("imp wrong place", CV, "Does the evidence support fail to the claim?", "implicit", "gd_check_covid/support", None),
    ("imp be-question", "Is this post hateful?", "Does this post fail to be hateful?", "implicit",
     "gd_hatemoji_build_v14/hateful", None),
    ("imp subordinate", "Does the assistant's reply confirm that the booking the customer asked for was actually made?",
     "Does the assistant's reply confirm that the booking the customer asked for failed to be actually made?",
     "implicit", "gd_multiwoz21_sysacts/booking", None),
    ("imp lack", "Does the reply contain a reference number?", "Does the reply lack a reference number?", "implicit",
     REPLY, "opposite"),
    ("imp fail to before contain", "Does the reply contain a reference number?",
     "Does the reply fail to contain a reference number?", "implicit", REPLY, "opposite"),
    ("imp lack wrong verb", "Does the reply show a reference number?", "Does the reply lack a reference number?",
     "implicit", REPLY_SHOW, None),
    ("imp lack same", "Do Ana Ruiz and Tomas Feld have the same nationality?",
     "Do Ana Ruiz and Tomas Feld lack the same nationality?", "implicit", CAPS_HAVE, None),
    ("imp inside the subject", CV, "Does the fail to evidence support the claim?", "implicit",
     "gd_check_covid/support", None),
    ("imp on the object", CV, "Does the evidence support the fail to claim?", "implicit", "gd_check_covid/support",
     None),
    ("ant ok", CV, "Does the evidence contradict the claim?", "antonym", "gd_check_covid/support", "opposite"),
    ("ant phrase", "Is the statement supported by the table?", "Is the statement refuted by the table?", "antonym",
     "gd_semtabfacts_sci/supported", "opposite"),
    ("ant off list", CV, "Does the evidence weaken the claim?", "antonym", "gd_check_covid/support", None),
    ("ant second pair", CV, "Does the evidence refute the claim?", "antonym", "gd_check_covid/support", "opposite"),
    ("ant wrong place", "Is the action being judged acceptable according to common social norms?",
     "Is the action being judged acceptable according to wrong social norms?", "antonym", "gd_sc101/acceptable", None),
    ("ant plus negation", CV, "Does the evidence not contradict the claim?", "antonym", "gd_check_covid/support", None),
    ("opt ok", "Of these two statements, does Statement 1 go against common sense?",
     "Of these two statements, does Statement 2 go against common sense?", "option_framing", "gd_comve/against",
     "opposite"),
    ("opt bad number", "Of these two statements, does Statement 1 go against common sense?",
     "Of these two statements, does Statement 3 go against common sense?", "option_framing", "gd_comve/against", None),
    ("eq ok", CV, "Is the claim backed up by the evidence?", "equiv", "gd_check_covid/support", "same"),
    ("eq drops quantifier",
     "Does this vehicle safety complaint report that at least one person was actually injured?",
     "Does this vehicle safety complaint state that a person was actually injured?", "equiv",
     "gd_nhtsa_complaints/injury", None),
    ("eq adds negation", CV, "Is the claim not backed by the evidence?", "equiv", "gd_check_covid/support", None),
    ("eq changes a name", "Were Ana Ruiz and Tomas Feld born in the same country?",
     "Were Ana Ruiz and Tom Feld born in the same country?", "equiv", HOT, None),
    ("eq introduces antonym", CV, "Does the evidence contradict the claim?", "equiv", "gd_check_covid/support", None),
    ("eq adds a frame", CV, "Is it true that the evidence supports the claim?", "equiv", "gd_check_covid/support",
     None),
    ("eq changes a quoted span",
     "According to the assistant's last message, is \"Friday at 7 pm\" confirmed for the customer's restaurant "
     "booking?",
     "Does the assistant's last message confirm \"Friday at 8 pm\" for the customer's restaurant booking?", "equiv",
     "gd_taskmaster1/status", None),
]


@pytest.mark.parametrize("case", HAND, ids=[c[0] for c in HAND])
def test_hand_cases_read_the_same_by_both_programs(case):
    _name, base, partner, kind, entry, want = case
    a, b = both(base, partner, kind, entry)
    if want is None:
        assert not (a == b == BL.relation_of(kind)), (a, b)
    else:
        assert (a, b) == (want, want)


def test_dev_frames_only_in_dev_mode():
    p = "Is it so that the evidence does not support the claim?"
    assert both(CV, p, "syntactic", "gd_check_covid/support", SRC.FRAMES_DEV) == ("opposite", "opposite")
    assert both(CV, "Is it true that the evidence does not support the claim?", "syntactic", "gd_check_covid/support",
                SRC.FRAMES_DEV) == (None, None)


def _mutants(partner: str) -> list:
    w = partner[:-1].split(" ")
    out = []
    if "not" in w:
        i = w.index("not")
        out.append(" ".join(w[:i] + w[i + 1:]) + "?")                       # cue removed
        out.append(" ".join(w[:i] + ["not"] + w[i:]) + "?")                 # second cue
        out.append(" ".join(w[:i] + ["never"] + w[i + 1:]) + "?")          # other cue
        for j in range(len(w)):                                             # cue moved anywhere else
            if j not in (i, i + 1):
                v = w[:i] + w[i + 1:]
                out.append(" ".join(v[:j] + ["not"] + v[j:]) + "?")
    out.append(" ".join(w[:-1]) + "?")                                      # last word dropped
    out.append("Do you think" + partner[len(partner.split(" that")[0]):])  # frame swapped
    return [m for m in out if m != partner]


def test_no_mutated_syntactic_partner_passes_both_programs():
    seen = 0
    for spec in FX.SPECS:
        src, q, decl = spec[0], spec[1], spec[5]
        if decl is None:
            continue
        e = SRC.entry_for({"source": src, "instructions": q})
        good = f"Is it true that{decl}?"
        assert both(q, good, "syntactic", e.key) == ("opposite", "opposite"), good
        for m in _mutants(good):
            assert not (both(q, m, "syntactic", e.key) == ("opposite", "opposite")), m
            seen += 1
    assert seen > 200


def test_exactly_one_fail_to_position_passes():
    for spec in FX.SPECS:
        src, q, implicit = spec[0], spec[1], spec[6]
        if implicit is None:
            continue
        e = SRC.entry_for({"source": src, "instructions": q})
        w = q[:-1].split(" ")
        ok = []
        for k in range(1, len(w) + 1):
            p = " ".join(w[:k] + ["fail", "to"] + w[k:]) + "?"
            if both(q, p, "implicit", e.key) == ("opposite", "opposite"):
                ok.append(p)
        assert ok == [implicit], (q, ok)


# ------------------------------------------------------------------------------------------------ selection

def test_every_base_rule_drops_with_its_reason():
    good = FX.rows()
    bad = FX.bad_rows()
    bases, rep = SEL.eligible(good + [r for r, _ in bad], FX.BAD_RELS, old_ids=FX.OLD_IDS, status=FX.keep_all,
                              strict_inputs=False)
    assert {b.row["id"] for b in bases} == {r["id"] for r in good}
    for row, reason in bad:
        _b, rep1 = SEL.eligible([row] + ([dict(row, id=row["id"] + "_other")] if reason == "call_id shared" else []),
                                FX.BAD_RELS, old_ids=FX.OLD_IDS, status=FX.keep_all, strict_inputs=False)
        assert any(reason in k for k in rep1["drop"]), (row["id"], reason, rep1["drop"])
    assert rep["kept"] == len(good) and sum(rep["drop"].values()) == len(bad)


def test_old_slice_by_group_and_state():
    good = FX.rows()
    import replay_sample as RS
    bases, rep = SEL.eligible(good, [], old_groups={good[0]["group_id"]}, old_states={RS.norm_state(good[1]["state"])},
                              status=FX.keep_all, strict_inputs=False)
    assert {b.row["id"] for b in bases} == {r["id"] for r in good[2:]}
    assert rep["drop"] == {"old slice (id or group)": 1, "old slice (normalised state)": 1}


def test_selection_with_the_real_register_status():
    bases, _ = SEL.eligible(FX.rows(), [], strict_inputs=False)
    assert len(bases) == len(FX.rows())


def test_missing_inputs_stop_the_build():
    """G0 H4: relations and the old slice (ids, groups, states) are required; an empty one stops the build."""
    good = FX.rows()
    with pytest.raises(ValueError):
        SEL.eligible(good, [], status=FX.keep_all)
    with pytest.raises(ValueError):
        SEL.eligible(good, FX.BAD_RELS, old_ids={"x"}, old_groups={"y"}, status=FX.keep_all)
    bases, _ = SEL.eligible(good, FX.BAD_RELS, old_ids={"x"}, old_groups={"y"}, old_states={"z"}, status=FX.keep_all)
    assert len(bases) == len(good)


# ------------------------------------------------------------------------------------------------ plan

def _plan_sig(plan):
    return [(i.pid, i.kind, i.frame, i.cue) for i in plan]


def _eligible(rows):
    return SEL.eligible(rows, [], status=FX.keep_all, strict_inputs=False)[0]


def test_plan_is_label_blind():
    pool = FX.many_rows(6)
    flipped = [dict(r, gold=1 - r["gold"]) for r in pool]
    eq = POOL.choices()
    p1, _ = SEL.plan_block(_eligible(pool), n_complement=40, n_equiv=15, equiv_pool=eq)
    p2, _ = SEL.plan_block(_eligible(flipped), n_complement=40, n_equiv=15, equiv_pool=eq)
    assert _plan_sig(p1) == _plan_sig(p2) and p1
    c1 = [BL.program_partner(i) for i in p1]
    c2 = [BL.program_partner(i) for i in p2]
    assert c1 == c2 and all(c1)                        # surfaces, cues and pool picks never read the gold


def test_plan_meets_quotas_and_caps_on_a_larger_pool():
    bases = _eligible(FX.many_rows(60))
    plan, rep = SEL.plan_block(bases, n_complement=140, n_equiv=60, seed="t37b-test", equiv_pool=POOL.choices())
    assert rep["pass"], rep
    assert rep["implicit_share"] >= 0.25 and rep["non_syntactic_share"] >= 0.30
    assert rep["complement"] <= 140 and rep["equiv"] <= 60
    assert len({i.base.row["id"] for i in plan}) == len(plan)
    for i in plan:
        assert i.kind in i.base.kinds
        if i.kind == "syntactic":
            assert i.frame in SRC.FRAMES_TRAIN
            assert i.frame not in SRC.FRAMES_EXCLUDED.get(i.base.entry.key, ())
        if i.kind == "equiv":
            assert i.base.entry.key not in SRC.NO_POOL and i.meta["para"]
    assert rep["equiv"] > 0


def test_plan_cuts_complements_to_keep_the_floors():
    bases = _eligible(FX.many_rows(20))
    no_implicit = [b for b in bases if "implicit" not in b.kinds]
    plan, rep = SEL.plan_block(no_implicit, n_complement=100, n_equiv=30, seed="t37b-test", source_cap=1.0,
                               template_cap=1.0, equiv_pool=POOL.choices())
    assert rep["complement"] == 0 and rep["equiv"] == 30
    assert rep["shortfall"]["complement"] == 100


def test_source_cap_holds_on_the_realised_block():
    bases = _eligible(FX.many_rows(80))
    plan, rep = SEL.plan_block(bases, n_complement=1400, n_equiv=600, seed="t37b-test", equiv_pool=POOL.choices())
    n = len(plan)
    assert rep["source_cap_ok"] and rep["template_cap_ok"]
    assert max(rep["by_source"].values()) <= max(1, int(0.10 * n))


# ------------------------------------------------------------------------------------------------ the in-memory flow

POOL = AP.Pool(FX.stand_in_pool())


def _flow(pool, *, mode="train", n_complement=12, n_equiv=4, **kw):
    bases = _eligible(pool)
    kw.setdefault("balance", False)                  # one stand-in row per question: no cell can hold both golds
    plan, prep = SEL.plan_block(bases, n_complement=n_complement, n_equiv=n_equiv, mode=mode,
                                equiv_pool=POOL.choices(), **kw)
    cands = BL.build_candidates(plan, mode=mode, records=POOL.records)
    return plan, cands


@pytest.fixture(scope="module")
def flow():
    plan, cands = _flow(FX.rows(), source_cap=1.0, template_cap=1.0)
    return plan, cands


def test_every_stand_in_candidate_passes_both_programs(flow):
    plan, cands = flow
    assert cands and all(c.ok for c in cands), [(c.item.pid, c.problems) for c in cands if not c.ok]
    assert {c.item.kind for c in cands} == set(SRC.KINDS)


def test_partner_rows_are_exact_and_load(flow):
    _plan, cands = flow
    rows, rels, rep = BL.finalize(cands, run_g15=True, trim=False)
    assert rep["dropped_at_finalize"] == [] and len(rows) == len(cands)
    by_id = {r["id"]: r for r in FX.rows()}
    for r, x in zip(rows, rels):
        t = r["meta"]["t37b"]
        base = by_id[t["base_id"]]
        assert BL.validate_partner(r, base) == []
        assert x == {"a": base["id"], "b": r["id"], "type": r["role"]}
        assert (r["call_id"], r["group_id"], r["state"]) == (base["call_id"], base["group_id"], base["state"])
        yes, no = SEL.parse_card(base["card"])
        if r["role"] == "complement":
            assert r["gold"] == 1 - base["gold"]
            if t["kind"] == "option_framing":
                assert r["card"] == base["card"]
            elif base["source"] == "gd_hotpotqa_yesno":
                assert SEL.parse_card(r["card"]) == SRC.COMPLEMENT_CARDS["gd_hotpotqa_yesno/q"]
            else:
                assert SEL.parse_card(r["card"]) == (no, yes)
        else:
            assert r["gold"] == base["gold"] and r["card"] == base["card"]
        assert R.g15_check(r)["ok"]
        assert r["meta"]["c2"]["author_mode"] == "T"
        if t["author"] == "haiku":
            assert t["kind"] == "equiv" and r["meta"]["c2"]["haiku_task_id"] and r["meta"]["wording_id"] != "t37b:equiv"
        else:
            assert t["kind"] in BL.PROGRAM_KINDS and r["meta"]["c2"]["haiku_task_id"] is None


def test_partner_rows_are_refused_when_the_gold_is_wrong(flow):
    _plan, cands = flow
    c = cands[0]
    r = BL.partner_row(c)
    base = c.item.base.row
    assert BL.validate_partner(r, base) == []
    bad = dict(r, gold=1 - r["gold"])
    assert any("gold" in p for p in BL.validate_partner(bad, base))


def _yn(v: int) -> str:
    return "yes" if v else "no"


def test_decide_branches(flow):
    _plan, cands = flow
    comp = next(c for c in cands if BL.relation_of(c.item.kind) == "opposite")
    eq = next(c for c in cands if c.item.kind == "equiv")
    g, ge = comp.item.base.row["gold"], eq.item.base.row["gold"]
    assert BL.decide(comp, "opposite", {"relation": "opposite"}, _yn(g), {"answer": _yn(1 - g)})[0] == "keep"
    assert BL.decide(comp, "opposite", "same", _yn(g), _yn(1 - g))[0] == "drop"
    assert BL.decide(comp, "opposite", "unclear", _yn(g), _yn(1 - g))[0] == "drop"
    assert BL.decide(comp, "opposite", "opposite", _yn(g), _yn(g))[0] == "review"
    assert BL.decide(comp, "opposite", "opposite", _yn(g), "maybe")[0] == "review"      # unreadable PARTNER answer
    assert BL.decide(comp, "opposite", "opposite", _yn(g), _yn(g), review="keep")[0] == "keep"
    assert BL.decide(comp, "opposite", "opposite", _yn(g), _yn(g), review="unsure")[0] == "drop"
    assert BL.decide(eq, "same", "same", _yn(ge), _yn(ge))[0] == "keep"
    assert BL.decide(eq, "same", "same", _yn(ge), _yn(1 - ge))[0] == "review"
    assert BL.decide(eq, "opposite", "same", _yn(ge), _yn(ge))[0] == "drop"


def test_blind_base_against_the_human_gold_drops_the_unit(flow):
    """G0 amendment A1-1 (fix F1): the blind solver's base answer must equal the base's human gold; a consistent pair
    is not enough, and no review can keep the unit. Only drops: the gold is never changed."""
    _plan, cands = flow
    comp = next(c for c in cands if BL.relation_of(c.item.kind) == "opposite")
    eq = next(c for c in cands if c.item.kind == "equiv")
    for c, rel, same in ((comp, "opposite", False), (eq, "same", True)):
        g = c.item.base.row["gold"]
        part = 1 - g if not same else g
        wrong = 1 - g
        # base answer = the gold, consistent partner: keep (the pilot-time behaviour)
        assert BL.decide(c, rel, rel, _yn(g), _yn(part))[0] == "keep"
        # base answer against the gold, partner consistent with that wrong base: dropped (this was kept before A1-1)
        wrong_part = 1 - wrong if not same else wrong
        v, why = BL.decide(c, rel, rel, _yn(wrong), _yn(wrong_part))
        assert v == "drop" and "human base gold" in why
        # base answer against the gold, inconsistent pair: dropped, not reviewed; review='keep' cannot rescue it
        assert BL.decide(c, rel, rel, _yn(wrong), _yn(1 - wrong_part))[0] == "drop"
        assert BL.decide(c, rel, rel, _yn(wrong), _yn(1 - wrong_part), review="keep")[0] == "drop"
        # base answer = the gold, inconsistent pair: still the Claude review path
        assert BL.decide(c, rel, rel, _yn(g), _yn(1 - part))[0] == "review"
        assert BL.decide(c, rel, rel, _yn(g), _yn(1 - part), review="keep")[0] == "keep"
        # A45 (b): an unreadable / missing base answer drops (it used to reach keep through the Claude review branch)
        assert BL.decide(c, rel, rel, "maybe", _yn(part))[0] == "drop"
        assert BL.decide(c, rel, rel, None, _yn(part), review="keep")[0] == "drop"


def test_haiku_items_carry_no_gold_state_or_card(flow):
    plan, cands = flow
    author = AP.author_batch()
    states = {c.item.base.row["state"] for c in cands}
    cards = {c.item.base.row["card"] for c in cands}
    for ch in author.chunks:
        for it in ch["items"]:
            assert set(it) == {"qid", "brief", "slots", "rules"}
            blob = repr(it)
            assert not any(s in blob for s in states) and not any(cd in blob for cd in cards)
    pa, pb = BL.polarity_batches(cands, seed="x")
    for b in (pa, pb):
        for ch in b.chunks:
            for it in ch["items"]:
                assert set(it) == {"qid", "question_a", "question_b"}
    assert pa.key != pb.key and [c["items"][0]["qid"] for c in pa.chunks] != [c["items"][0]["qid"] for c in pb.chunks]
    pairs = [(it["question_a"], it["question_b"]) for ch in pa.chunks for it in ch["items"]]
    assert len(pairs) == len(set(pairs))                 # one judgement per distinct question pair (G0 H41)
    ba, bp = BL.blind_batches(cands, seed="x")
    for b in (ba, bp):
        for ch in b.chunks:
            for it in ch["items"]:
                assert "gold" not in it and set(it) <= {"qid", "kind", "text", "question", "definitions"}
    with pytest.raises(chunker.ChunkError):
        chunker.make_batch("polarity", "T37b", [("x", {"question_a": "a?", "question_b": "b?", "gold": 1})],
                           seed="s", prompt="p")


def test_program_written_partners_need_no_haiku(flow):
    _plan, cands = flow
    for c in cands:
        assert c.author == ("haiku" if c.item.kind == "equiv" else "program")
        if c.item.kind == "syntactic":
            assert c.question in PA.syntactic_targets(c.item.base.row["instructions"], c.item.base.entry, c.item.frame)
        if c.item.kind == "implicit":
            assert c.question in PA.implicit_targets(c.item.base.row["instructions"], c.item.base.entry)
            assert c.item.cue in c.question
        if c.item.kind == "equiv":
            assert c.haiku_task_id and c.pair == (SRC.pool_template(c.item.base.entry)[0], c.item.meta["para_text"])


def test_judged_pool_pairs_are_not_read_again(flow):
    _plan, cands = flow
    judged = POOL.judged
    items = BL.polarity_items(cands, judged)
    assert items and not any(k in judged for k, _ in items)
    eq = [c for c in cands if c.item.kind == "equiv"]
    assert eq and all(BL.polarity_of(c, {}, {}, judged) == ("same", "same") for c in eq)
    comp = next(c for c in cands if c.item.kind == "syntactic")
    k = BL.pair_key(*comp.pair)
    assert BL.polarity_of(comp, {k: {"relation": "opposite"}}, {k: "opposite"}) == ({"relation": "opposite"},
                                                                                     "opposite")


def test_frames_excluded_for_normative_entries():
    """G0 H25: 'Is it right to say that' never frames a gd_sc101 acceptable / wrong partner."""
    for k in SRC.FRAMES_EXCLUDED:
        assert "Is it right to say that" not in SEL.frames_for(E[k], TRAIN)
    pool = [b for b in _eligible(FX.many_rows(30)) if b.entry.key in SRC.FRAMES_EXCLUDED
            or b.entry.source == "gd_nhtsa_complaints"]
    plan, _ = SEL.plan_block(pool, n_complement=120, n_equiv=0, source_cap=1.0, template_cap=1.0)
    frames = {i.frame for i in plan if i.kind == "syntactic" and i.base.entry.key in SRC.FRAMES_EXCLUDED}
    assert frames and "Is it right to say that" not in frames


SCOPE = SRC.Entry("gd_test", "q", r"[^?]+\?", ("syntactic", "equiv"), subject="the evidence")


@pytest.mark.parametrize("word,ok", [("all", False), ("every", False), ("each", False), ("any", True),
                                     ("either", True)])
def test_quantifier_scope_after_not(word, ok):
    """G0 H28: after the inserted 'not' only quantifiers with one natural not(...) reading are allowed."""
    base = f"Does the evidence support {word} claim?"
    partner = f"Is it true that the evidence does not support {word} claim?"
    a, b = both(base, partner, "syntactic", SCOPE)
    assert (a == b == "opposite") == ok, (a, b)


def test_trim_block_restores_floors_and_caps(flow):
    plan, _ = flow
    bases = _eligible(FX.many_rows(60))
    big, _ = SEL.plan_block(bases, n_complement=140, n_equiv=60, seed="t37b-test", equiv_pool=POOL.choices())
    imp = [i for i in big if i.kind == "implicit"]
    gone = {id(i) for i in imp[: max(1, len(imp) // 2)]}
    kept, removed = SEL.trim_block([i for i in big if id(i) not in gone])
    rep = SEL.plan_report(kept, n_complement=140, n_equiv=60)
    assert removed and rep["floors_ok"] and rep["source_cap_ok"] and rep["template_cap_ok"]
    assert all(why.startswith(("floors", "source cap", "template cap")) for _p, why in removed)
    assert SEL.max_comp(250, 400) == 1000 and not SEL.floors_ok(250, 400, 1001) and SEL.floors_ok(251, 301, 1001)


def test_local_bans_drop_a_partner(flow):
    _plan, cands = flow
    c = next(x for x in cands if x.item.kind == "equiv")
    bad = BL.check_candidate(c.item, "Should the statement that the claim is backed up by the evidence be rejected?",
                             author="haiku", frames=TRAIN)
    assert not bad.ok


# ------------------------------------------------------------------------------------------------ dev mode and writer

def test_dev_mode_uses_held_out_frames_and_is_never_trained():
    plan, cands = _flow(FX.rows(), mode="dev", n_complement=10, n_equiv=0)
    assert plan and all(i.kind in ("syntactic", "antonym") for i in plan)
    assert all(i.frame in SRC.FRAMES_DEV for i in plan if i.kind == "syntactic")
    rows, _rels, rep = BL.finalize([c for c in cands if c.ok], mode="dev", run_g15=False)
    assert rows and rep["pass"]
    for r in rows:
        assert r["meta"]["dev_only"] is True
        assert any("dev-only" in p for p in R.validate_row(r, training=True))


def test_writer_refuses_before_a38(flow):
    _plan, cands = flow
    rows, rels, _ = BL.finalize(cands, run_g15=False)
    with pytest.raises(paths.DataBeforeFreeze):
        BL.write_block(rows, rels, prereg_text="no freeze ruling in this text")
    with pytest.raises(paths.DataBeforeFreeze):
        BL.write_dev([], rows, rels, prereg_text="no freeze ruling in this text")
    if not paths.a38_frozen():
        with pytest.raises(paths.DataBeforeFreeze):
            BL.write_block(rows, rels)


def test_writers_refuse_on_a_g0_problem(flow, monkeypatch):
    """G0 H1: a failing g0_problems() halts every writer before anything is written."""
    _plan, cands = flow
    rows, rels, _ = BL.finalize(cands, run_g15=False)
    monkeypatch.setattr(BL, "G0_SHA256", "0" * 64)
    a38 = "> **Ruling A38 (test text)"
    for call in (lambda: BL.write_block(rows, rels, prereg_text=a38),
                 lambda: BL.write_dev([], rows, rels, prereg_text=a38),
                 lambda: AP.write_author_tasks(prereg_text=a38)):
        with pytest.raises(RuntimeError):
            call()


def test_write_dev_refuses_training_rows(flow):
    _plan, cands = flow
    rows, rels, _ = BL.finalize(cands, run_g15=False)
    with pytest.raises(ValueError):
        BL.write_dev([], rows, rels, prereg_text="> **Ruling A38 (test text)")


def test_template_strings_list_every_piece():
    t = BL.template_strings()
    assert t["frames_train"] == list(SRC.FRAMES_TRAIN) and t["frames_dev"] == list(SRC.FRAMES_DEV)
    assert t["complement_cards"] and t["antonyms"] and len(t["prompts"]) == 4 and t["pool_templates"]


def test_flow_is_deterministic():
    p1, c1 = _flow(FX.rows(), source_cap=1.0, template_cap=1.0)
    p2, c2 = _flow(FX.rows(), source_cap=1.0, template_cap=1.0)
    assert [BL.partner_row(c)["id"] for c in c1] == [BL.partner_row(c)["id"] for c in c2]
