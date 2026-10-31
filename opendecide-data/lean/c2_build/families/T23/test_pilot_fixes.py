"""families/T23/test_pilot_fixes.py: the Stage B pilot fix iteration 1 of T23 (G0 v4; PILOT_VERDICT FIX-1 to FIX-4 and the
kit-level fixes), on the REAL frozen pools_v2 (read through the pilot loader; nothing is written, no Haiku, no network).

  wording screen  c2_kit.polarity on the 159 admitted yes/no wordings: P1-P3 clean; the 13 double negations of the shape
                  "is X not a ... that does not ..." (negated question frame) are quarantined, 14 stay (>= 3 per form);
                  the rule itself on the wrong shapes
  FIX-1           a double-negation wording is never drawn for a row whose complement is antonym or implicit; the units
                  of such rows pass G-TW
  FIX-2           yn_version proposes the syntactic complement only; the other forms keep both kinds (>= 30% non-syntactic)
  FIX-3           author mode (F 20%) and register drawn from the row key; no register above the 15% cap
  FIX-4           yes/no rows carry the rules in row.card, choice rows in the instructions; solver B refuses a card that
                  does not fit the record; the family mean is under 800 real tokens
Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T23/test_pilot_fixes.py
"""
from __future__ import annotations

import collections
import os
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from c2_kit import cards as CK  # noqa: E402
from c2_kit import pipeline, polarity  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.distractors import uhash  # noqa: E402
from families.T23 import plugin as P  # noqa: E402
from families.T23 import solver_b as B  # noqa: E402

HERE = Path(__file__).resolve().parent
TOKENIZER = Path(os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/"
                                    "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json"))
TRAINING = ("S1", "S2", "S3", "S4")
# the 13 wordings G0 section 11 quarantines (qform#id suffix)
QUARANTINED = {"yn_version": ("2c822bb7", "5b7759ca", "8d3f3916", "a716edc2"),
               "yn_claim": ("628c8724", "84f76171", "88ec11aa", "9c2bd84c", "aba6f0ab"),
               "yn_outcome": ("66b8802b", "7b90581b", "e737d26e", "ea145c1a")}


@pytest.fixture(scope="module")
def kit():
    with PL.open_family("T23") as k:
        yield k


@pytest.fixture(scope="module")
def plugin(kit):
    return kit.plugin


@pytest.fixture(scope="module")
def ctx(kit):
    return kit.ctx


def _wordings(ctx, qform):
    return [s for s in ctx.skins.values() if s.kind == "wording" and s.qform == qform]


# ------------------------------------------------------------------------------------------------ the wording screen

def test_the_screen_quarantines_exactly_the_13_double_negations(plugin, ctx):
    assert polarity.enabled(plugin) and polarity.config_problems(plugin) == []
    kept, bad_p123 = polarity.screen(ctx, plugin)
    assert bad_p123 == {}, bad_p123                                    # P1-P3: every admitted wording reads right
    yn = [s for s in ctx.skins.values() if s.kind == "wording" and P.QF[s.qform].qtype == "noul"]
    assert len(yn) == 159
    bad = plugin.quarantined_wordings(ctx)
    want = {f"T23-WD-q.t23.{qf}#{h}" for qf, hs in QUARANTINED.items() for h in hs}
    assert set(bad) == want and len(bad) == 13
    assert all(p == [P.DN_FRAME_PROBLEM] for p in bad.values())
    ent = plugin._entry(ctx)
    assert len(ent.screened.skins) == len(ctx.skins) - 13
    kept_dn = collections.Counter(ctx.skins[s].qform for s in ent.dn)
    assert kept_dn == {"yn_version": 5, "yn_claim": 4, "yn_outcome": 5}   # the G0 quota needs >= 3 per positive form
    assert not set(ent.narrow.skins) & ent.dn and set(ent.narrow.skins) <= set(ent.screened.skins)
    for sid in ent.dn:                       # the 14 that stay: two cancelling negations under an explicit outer frame
        r = polarity.read(ctx.skins[sid].text, P.NEGATIVE_PREDICATES)
        assert r.k_syn == 2 and not r.lexical and r.frame in ("plain", "explicit"), ctx.skins[sid].text
    g0 = (HERE / "G0_SPEC.md").read_text(encoding="utf-8")
    sec = g0[g0.index("## 11."):]
    for qf, hs in QUARANTINED.items():
        for h in hs:
            assert h in sec, (qf, h)


@pytest.mark.parametrize("text,pol,code", [
    ("Is {CANDIDATE} not a version that does not govern the case in {CASE_ID}?", +1, "P4"),        # the quarantined shape
    ("Is the claim to check not a claim that the governing version does not support?", +1, "P4"),
    ("Is it the case that it is not the case that {CANDIDATE} does not decide this case?", +1, None),
    ("Is it not the case that the governing version does not conflict with the claim to check?", +1, "P1"),
    ("Does the governing version contradict the claim to check?", +1, "P2"),
    ("Does the governing version contradict the claim to check?", -1, None),
    ("Is case {CASE_ID} outside the {TERM_LABEL} set by the governing version?", -1, None),
    ("Is case {CASE_ID} not outside the {TERM_LABEL} set by the governing version?", -1, "P4,P1"),
    ("Isn't {CANDIDATE} the governing version for this case?", +1, "P3,P2"),
    ("Is this case governed by some version besides {CANDIDATE}?", -1, None),
])
def test_the_polarity_rule_on_the_t23_shapes(text, pol, code):
    probs = polarity.problems(text, pol, negatives=P.NEGATIVE_PREDICATES, strict_frames=True)
    assert [p[:2] for p in probs] == (code.split(",") if code else []), (text, probs)


def test_render_refuses_a_quarantined_wording(plugin, ctx):
    spec = next(s for s in (plugin.sample(k, "S1") for k in range(200)) if s.qform == "yn_version")
    wd = ctx.skin("T23-WD-q.t23.yn_version#2c822bb7")
    with pytest.raises(K.RenderError):
        plugin.render(spec, ctx, wording=wd)
    assert plugin.render(spec, ctx).row["meta"]["wording_id"] not in plugin.quarantined_wordings(ctx)


# ------------------------------------------------------------------------------------------------ FIX-1 and FIX-2

def test_no_double_negation_meets_a_non_syntactic_complement(plugin, ctx):
    """FIX-1: ctx_for() hides the double-negation wordings from a row whose proposed complement is antonym / implicit;
    those units pass G-TW (the partner differs from the base by exactly the cues the form declares)."""
    checked = would_hit = 0
    for seed in range(300):
        for smp in TRAINING:
            spec = plugin.sample(seed, smp)
            comp = plugin._complement_form(spec)
            if comp is None or P.QF[comp].complement_kind == "syntactic":
                continue
            narrow = plugin.ctx_for(spec, ctx)
            assert narrow is not plugin._entry(ctx).screened
            key = plugin._row_key(spec)
            got = narrow.pick("T23", "wording", key, qform=spec.qform)
            assert polarity.read(got.text, P.NEGATIVE_PREDICATES).k_syn < 2, got.text
            full = plugin._entry(ctx).screened.pick("T23", "wording", key, qform=spec.qform)
            would_hit += polarity.read(full.text, P.NEGATIVE_PREDICATES).k_syn >= 2
            checked += 1
            if checked <= 150:
                res = pipeline.build_unit(plugin, spec, ctx, run_g15=False)
                assert res.ok, (seed, smp, res.problems)
    assert checked > 100 and would_hit > 10, (checked, would_hit)      # the filter was needed, and it is applied


def test_yn_version_proposes_only_the_syntactic_complement(plugin):
    kinds = collections.defaultdict(collections.Counter)
    for seed in range(1500):
        for smp in TRAINING:
            spec = plugin.sample(seed, smp)
            for p in plugin.relations(spec):
                if p.kind == "complement":
                    kinds[spec.qform][p.qform] += 1
    assert set(kinds["yn_version"]) == {"yn_version_not"}
    assert set(kinds["yn_claim"]) == {"yn_claim_contra", "yn_claim_not"}
    assert set(kinds["yn_outcome"]) == {"yn_outcome_out", "yn_outcome_not"}
    n_all = sum(sum(c.values()) for c in kinds.values())
    non_syn = sum(v for c in kinds.values() for q, v in c.items() if P.QF[q].complement_kind != "syntactic")
    assert non_syn / n_all >= 0.30, non_syn / n_all                  # spec 4.1: >= 30% non-syntactic complement pairs
    assert "yn_version_other" in P.QF and P.QF["yn_version_other"].complement_kind == "implicit"


# ------------------------------------------------------------------------------------------------ FIX-3

class _Stub:
    def __init__(self, sampler):
        self.sampler = sampler


def test_author_mode_and_register_come_from_the_row_key(plugin, ctx):
    ent_ctx = plugin._entry(ctx).screened
    n = collections.Counter()
    modes, regs = collections.Counter(), collections.Counter()
    for sampler in TRAINING:
        for seed in range(3000):
            key = f"T23|{seed}|{sampler}|ch_version"
            sk = plugin._pick_skin(ent_ctx, _Stub(sampler), key, False)
            want_mode = "F" if uhash(key, "mode") < P.P_MODE_F else "T"
            assert sk.author_mode == want_mode and not sk.held_out and sk.kind == "skin"
            if sampler == "S4":
                assert sk.register in P.S4_REGISTERS
            else:
                assert sk.register in dict(P.REGISTER_WEIGHTS[want_mode])        # never the fallback
            modes[sk.author_mode] += 1
            regs[sk.register] += 1
            n[sampler] += 1
    total = sum(modes.values())
    assert 0.185 <= modes["F"] / total <= 0.215, modes
    assert max(regs.values()) / total <= 0.15 and min(regs.values()) / total >= 0.05, regs
    ho = plugin._pick_skin(ent_ctx, _Stub("S5"), "T23|1|S5|ch_term", True)
    assert ho.held_out and ho.author_mode == "T"
    for mode, weights in P.REGISTER_WEIGHTS.items():
        assert abs(sum(w for _, w in weights) - 1.0) < 1e-9
    assert set(dict(P.REGISTER_WEIGHTS["T"])) == {s.register for s in ctx.skins.values()
                                                  if s.kind == "skin" and s.author_mode == "T" and not s.held_out}
    assert set(dict(P.REGISTER_WEIGHTS["F"])) == {s.register for s in ctx.skins.values()
                                                  if s.kind == "skin" and s.author_mode == "F"}


# ------------------------------------------------------------------------------------------------ FIX-4

def _rows(plugin, ctx, n=240):
    out = []
    for seed in range(n // len(TRAINING)):
        for smp in TRAINING:
            spec = plugin.sample(seed, smp)
            out.append((spec, plugin.render(spec, plugin.ctx_for(spec, ctx))))
    return out


def test_the_rules_sit_where_the_served_prompt_prints_them_once(plugin, ctx):
    seen = collections.Counter()
    for spec, rr in _rows(plugin, ctx):
        row = rr.row
        card = K.fill(plugin.card_template(spec), spec.all_slots(), rr.forms).text
        if row["qtype"] == "noul":
            assert row["card"] == card and "\n\n" not in row["instructions"], spec.qform
            assert row["meta"]["defs_style"] == "rules_in_card_full"
            assert CK.split_rules(row) == (card, row["instructions"])
        else:
            assert row["card"] is None and row["instructions"].startswith(card + "\n\n")
            assert row["meta"]["defs_style"] == "rules_in_instructions_full"
            assert CK.split_rules(row) == (card, row["instructions"][len(card) + 2:])
        assert P.CLOSED_WORLD in card
        seen[(row["qtype"], spec.structure["clause"] is not None, spec.qform in P.CLAIM_FORMS,
              spec.qform in P.OUTCOME_FORMS)] += 1
    assert len({k for k in seen if k[0] == "noul"}) >= 4 and len({k for k in seen if k[0] == "choice"}) >= 2, seen


def test_solver_b_refuses_a_card_that_does_not_fit_the_record(plugin, ctx):
    rows = {}
    for spec, rr in _rows(plugin, ctx, 400):
        q = spec.qform
        key = (rr.row["qtype"], spec.structure["clause"] is not None, q in P.CLAIM_FORMS, q in P.OUTCOME_FORMS)
        rows.setdefault(key, (spec, rr))
    yn_claim = next(v for k, v in rows.items() if k[0] == "noul" and k[2] and k[1])
    yn_plain = next(v for k, v in rows.items() if k[0] == "noul" and not k[1] and not k[2] and not k[3])
    choice = next(v for k, v in rows.items() if k[0] == "choice")
    for _spec, rr in (yn_claim, yn_plain, choice):
        assert B.solve_b(B.parse(rr.row, ctx)) == rr.answer                                  # untouched rows parse
    row = yn_claim[1].row
    lines = row["card"].split("\n")
    claim_line = next(ln for ln in lines if ln.startswith("- A claim about"))
    clause_line = next(ln for ln in lines if ln.startswith("- At most one clause"))
    for bad in (dict(row, card=row["card"].replace(claim_line + "\n", "")),                    # claim line missing
                dict(row, card=row["card"].replace(clause_line + "\n", "")),                   # clause line missing
                dict(row, card=None, instructions=row["card"] + "\n\n" + row["instructions"]),  # rules in the instructions
                dict(row, card=row["card"] + "\n- A claim about the term is supported always.")):
        with pytest.raises(B.ParseError):
            B.parse(bad, ctx)
    plain = yn_plain[1].row
    extra = plain["card"].replace("\nOnly the listed", "\n- A claim about the x is supported when y.\nOnly the listed")
    with pytest.raises(B.ParseError):
        B.parse(dict(plain, card=extra), ctx)                                  # a rule line the question cannot use
    ch = choice[1].row
    with pytest.raises(B.ParseError):
        B.parse(dict(ch, card="x"), ctx)                                       # a card on a choice row
    with pytest.raises(B.ParseError):
        B.parse(dict(ch, instructions=ch["instructions"].split("\n\n")[-1]), ctx)  # the rules dropped from a choice row


@pytest.mark.skipif(not TOKENIZER.is_file(), reason="local Qwen tokenizer file not cached")
def test_family_mean_is_under_800_tokens_and_mode_f_under_25_percent(kit):
    b = pilot.build_pilot(kit, 300, seed_base=900000, run_g15=False)
    assert b.stats["drops_by_gate"] == {}, b.stats["drops_by_gate"]
    rows = [i.row for i in b.infos]
    rep = CK.token_report(rows)
    assert rep["counted_by"].startswith("mixer.token_counts") and rep["mean"] <= 800 and rep["max"] <= 2000, rep
    assert rep["rules_mean"]["choice"] <= 175 and rep["rules_mean"]["yes_no"] <= 175, rep
    f = sum(1 for r in rows if r["meta"]["c2"]["author_mode"] == "F") / len(rows)
    assert f <= 0.25, f
    assert {r["meta"]["defs_style"] for r in rows} == {"rules_in_card_full", "rules_in_instructions_full"}
    assert rows[0]["meta"]["spec_id"] == "T23.G0lite." + P.T23.G0_SHA256[:8]
