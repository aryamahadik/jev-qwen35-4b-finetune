"""F4 gen3_polarity_ladder: the frames (pl_frames), the propositions (pl_sources) and the builder
(gen3_polarity_ladder) on a small in-memory build. CPU only; nothing is written (the builder never writes unless
main(--write) is called)."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
for p in (str(LEAN / "golden_src" / "gen3"), str(LEAN / "yn2b"), str(LEAN)):
    if p not in sys.path:
        sys.path.insert(0, p)
import gen3_polarity_ladder as g  # noqa: E402
import mv_core as mv  # noqa: E402
import pl_frames as pf  # noqa: E402
import pl_sources as ps  # noqa: E402

JUDGE_RX = re.compile(r"\b(right|wrong|correct|incorrect|accurate|inaccurate|mistaken|reply|replies|agreed|disagree|"
                      r"undercut|debate|commenter|back)\b", re.I)


# ------------------------------------------------------------------------------------------------ frames
def test_frame_inventory():
    fams = Counter(q["family"] for q in pf.QUADS)
    assert set(fams) == set(pf.FAMILIES) and len(fams) == 10 and all(v == 3 for v in fams.values())
    assert len(pf.TRAIN_FAMILIES) == 8 and set(pf.HOLDOUT_FAMILIES) == {"audit_finding", "counter_hypothesis"}
    assert sum(pf.FAMILIES[f] for f in pf.HOLDOUT_FAMILIES) == 1          # one record family held out
    assert sum(pf.FAMILIES[f] for f in pf.TRAIN_FAMILIES) == 3
    assert len({q["id"] for q in pf.QUADS}) == 30


def test_every_cell_is_well_formed():
    for t in pf.all_templates():
        for k in ("text", "yes", "no"):
            assert t[k].count("{d}") == 1, (t["quad"], t["cell"], k)
            assert "{A}" not in t[k] and "{B}" not in t[k]
            assert t[k][0].isupper()
        assert t["text"].endswith("?") and t["yes"].endswith(".") and t["no"].endswith(".")
    for q in pf.QUADS:
        texts = {pf.cell_templates(q["id"], c)[0] for c in pf.CELLS}
        assert len(texts) == 4, q["id"]


def test_no_banned_or_dialogue_words_in_any_frame():
    for t in pf.all_templates():
        for k in ("text", "yes", "no"):
            assert not JUDGE_RX.search(t[k]), (t["quad"], k, t[k])
            assert "two notes" not in t[k].lower()
            assert not pf.SPEAKER_LABEL.search(t[k]), t[k]
            assert not mv.judge_violations(t[k])


def test_gold_is_truth_xor_flips():
    assert [pf.gold(True, c) for c in pf.CELLS] == [True, False, False, True]
    assert [pf.gold(False, c) for c in pf.CELLS] == [False, True, True, False]
    assert pf.CELL_ROLE == {"00": "para", "10": "neg", "01": "neg", "11": "dneg"}


@pytest.mark.parametrize("qid,cell,truth,answer", [
    ("dd1", "00", True, "yes"),    # is it established that P?
    ("dd1", "10", True, "no"),     # is it excluded that P?
    ("dd1", "01", True, "no"),     # is it established that it does not hold that P?
    ("dd1", "11", True, "yes"),    # is it excluded that it does not hold that P?
    ("gk1", "10", False, "yes"),   # gate admits exactly when P; it turned the item away; did it act properly?
    ("gk1", "11", True, "yes"),    # ... turned away, acted improperly? (P true: the item should have been admitted)
    ("vr3", "01", False, "yes"),   # determination P contradicted by the material? (P false)
    ("so2", "10", True, "no"),     # mark beside P reads refused; should it be kept as it is? (P true)
    ("ck1", "01", True, "no"),     # item says P; ticked as not done? (P true)
    ("ch1", "10", False, "yes"),   # someone who denied that P has to keep that view? (P false)
])
def test_frames_read_as_intended(qid, cell, truth, answer):
    """Hand-read semantics of a sample of cells (independent of CELL_FLIPS): the rendered question with a known P."""
    q, y, n = pf.render(qid, cell, "the proposed call may run under the policy")
    assert "the proposed call may run under the policy" in q
    assert g._yn(pf.gold(truth, cell)) == answer, q


def test_holdout_families_share_no_6gram_with_training_families():
    import check_yn2b as cy
    tr = set().union(*[cy.runs(t["text"]) | cy.runs(t["yes"]) | cy.runs(t["no"])
                       for t in pf.all_templates(pf.TRAIN_FAMILIES)])
    for t in pf.all_templates(pf.HOLDOUT_FAMILIES):
        assert not (cy.runs(t["text"]) & tr), (t["quad"], t["cell"], sorted(cy.runs(t["text"]) & tr)[:2])


def test_template_cue_shares_under_60_percent_at_the_build_mix():
    """Row-level cue shares at the build's ladder mix (para 50%, negA 12.5%, negB 12.5%, dneg 25%)."""
    import build_v11_fixes as b
    w = {"00": 4, "10": 1, "01": 1, "11": 2}
    items = []
    for t in pf.all_templates():
        items += [(t["text"], t["flips"])] * w[t["cell"]]
    sh = {k: v for k, v in b.cue_shares(items).items() if v[1] >= 8}
    worst = max(sh.items(), key=lambda kv: kv[1][0])
    assert worst[1][0] <= 0.60, worst


def test_frames_share_no_6gram_with_reference_sets():
    """SPEC 5 F4 / 7.3: dialogue_rebuttal, v11 train templates, ship-split instructions, OHS-1/2 instructions and
    cards, eval injected spans (check_yn2b.template_refs; OHS-3 is not part of it)."""
    import check_yn2b as cy
    refs = cy.template_refs(LEAN)
    allr = set().union(*refs.values())
    for t in pf.all_templates():
        assert not (cy.runs(t["text"]) & allr), (t["quad"], t["cell"])


# ------------------------------------------------------------------------------------------------ propositions
def _row(tpl, ins, qkind="yn", pol=0, role="aff", view="base"):
    return {"instructions": ins, "meta": {"tpl": tpl, "qkind": qkind, "polarity": pol, "role": role, "view": view}}


@pytest.mark.parametrize("key,tpl,ins,kind,P", [
    ("gen3_rule_chain", "pos1", 'Under the fee code, is the outcome of this application "full waiver of the fee"?',
     "f1.outcome", 'the outcome of this application under the fee code is "full waiver of the fee"'),
    ("gen3_rule_chain", "pos3", 'Does the fence bylaw give this fence request the outcome "approved", rather than a '
                                'different one?', "f1.outcome",
     'the outcome of this fence request under the fence bylaw is "approved"'),
    ("gen3_rule_chain", "jdg2", "Is the decision recorded for this damage claim supported by the claims tariff when it "
                                "is applied to the case file?", "f1.record",
     "the decision recorded in the case file for this damage claim is consistent with the claims tariff"),
    ("gen3_rule_chain", "bpos1", "Under the rules in the card, does the evidence establish the claim?", "f1b.claim",
     "under the rules in the card, the evidence establishes the claim"),
    ("gen3_tool_guard", "may4", "Under these rules, is the guardrail free to let the proposed call through?", "f2.may",
     "the proposed call may run under the policy"),
    ("gen3_tool_guard", "output1", "Is every stated requirement met by the assistant's output?", "f2.output",
     "the assistant's output meets every requirement stated for it"),
    ("gen3_def_literal", "is0", "Under Rule 16 of the Procurement Rules of Eastholm Council, is the bid a 'compliant "
                                "tender'?", "f6.term",
     "the bid is a 'compliant tender' under Rule 16 of the Procurement Rules of Eastholm Council"),
    ("gen3_def_literal", "is1", "Going by the definition in Standard 36 and not by everyday usage, is the post 'spam'?",
     "f6.term", "the post is 'spam' by the definition in Standard 36, not by everyday usage"),
    ("gen3_def_literal", "judge4", "Is the entry in the incident register for this incident backed by Section 19 as "
                                   "written?", "f6.record",
     "the entry in the incident register for this incident is backed by Section 19 as written"),
    ("gen3_state_track", "inv.ge.a", "Are at least 5 units of SKU-781819 available at the end of the log?",
     "f3.state", "at least 5 units of SKU-781819 are available at the end of the log"),
    ("gen3_state_track", "tck.ow.b", "Under the numbered rules, does ticket TCK-729297 belong to Zisel Furkley at the "
                                     "end of the log?", "f3.state",
     "Zisel Furkley owns ticket TCK-729297 at the end of the log"),
    ("gen3_state_track", "agt.eq.b", "Under the numbered rules, does the shared folder hold invoice-4879.pdf at the "
                                     "end of the session?", "f3.state",
     "invoice-4879.pdf is in the shared folder at the end of the session"),
    ("gen3_state_track", "jdg.a", "Is the agent's recorded state consistent with the log under the numbered rules?",
     "f3.record", "the agent's recorded state is consistent with the log under the numbered rules"),
])
def test_propositions(key, tpl, ins, kind, P):
    assert ps.proposition(key, _row(tpl, ins)) == (kind, P)


def test_propositions_refused():
    assert ps.proposition("gen3_tool_guard", _row("confirm0", "Is a missing valid user confirmation the only reason "
                                                               "the guardrail must block the proposed call?")) is None
    assert ps.proposition("gen3_tool_guard", _row("block0", "Under the policy, must the guardrail block the proposed "
                                                            "call?", pol=1, role="neg")) is None
    assert ps.proposition("gen3_tool_guard", _row("may0", "Under the policy, may the guardrail let the proposed call "
                                                          "run?", view="attack")) is None
    assert ps.proposition("gen3_rule_chain", _row("pos1", "Something else entirely?")) is None


def test_fmt_regex_round_trip():
    rx = ps.fmt_regex("Is {s} the owner of ticket {e} {when}?")
    m = rx.match("Is Ann Bo the owner of ticket TCK-1 at 2026-01-02T03:04:00Z?")
    assert m.groupdict() == {"s": "Ann Bo", "e": "TCK-1", "when": "at 2026-01-02T03:04:00Z"}
    assert ps.fmt_regex("{a} and {a}").match("x and x") and not ps.fmt_regex("{a} and {a}").match("x and y")


def test_every_written_affirmative_source_row_gets_a_proposition():
    """F3 / F1 / F6 every polarity-0 yes/no row; F2 every row except the confirmation-only predicate."""
    for key in ps.B_FAMILIES:
        for part in ("train", "dev"):
            if not mv.raw_paths(key, part)[0].exists():
                pytest.skip(f"{key} not written")
            rows, _ = mv.read_raw(key, part)
            miss = [r["meta"]["tpl"] for r in rows if r["meta"]["qkind"] == "yn" and r["meta"]["polarity"] == 0
                    and r["meta"]["view"] != "attack" and r["meta"]["role"] in ("aff", "para")
                    and ps.proposition(key, r) is None]
            if key == "gen3_tool_guard":
                miss = [t for t in miss if not t.startswith("confirm")]
            assert not miss, (key, part, Counter(miss).most_common(3))


def test_a_sources_are_clean():
    for s, spec in ps.A_SOURCES.items():
        assert s.startswith("gd_") and not s.startswith("gd_gen")
        assert len(spec["defs"]) >= 3
        for k, v in spec["defs"].items():
            assert k == k.strip() and ": " not in k and k.lower() not in ("yes", "no", "task")
            assert "\n" not in v and v.endswith(".") and not mv.judge_violations(k, v)
        assert not mv.judge_violations(spec["task"]) and "\n" not in spec["task"]
        P = ps.a_proposition(s, next(iter(spec["defs"])))
        assert P.startswith('"') and P.endswith(" best")
    assert set(ps.A_SOURCES).isdisjoint({"clinc150", "banking77", "std_hate", "gd_ghc_hate", "tb_label_nli"})


def test_a_sources_not_name_matched_with_dev_splits():
    dev = g.dev_source_names()
    assert dev, "the ship splits are needed for this check"
    assert g.name_matched(ps.A_SOURCES, dev) == {}
    # the rule itself catches the SPEC's named sources
    assert g.name_matched(["gd_ghc_hate", "tb_label_nli"], {"ghc_hate", "tb_label_nli_x"})


def test_a_definitions_share_no_12gram_with_dev_or_held_sets():
    d = g.Decon(True)
    for s, spec in ps.A_SOURCES.items():
        for k, v in list(spec["defs"].items()) + [("task", spec["task"])]:
            assert not d.text_hit(f"- {k}: {v}"), (s, k)


# ------------------------------------------------------------------------------------------------ small build
SMALL = {"train": 40, "dev_iid": 12, "dev_holdout": 12}


@pytest.fixture(scope="module")
def pools():
    return g.load_b_pool(), g.load_a_pool()[0]


def small_build(pools):
    fb = mv.FamilyBuilder(g.KEY, generator_file=g.__file__)
    return g.build(targets=SMALL, fb=fb, b_pool=pools[0], a_pool=pools[1], decon=g.Decon(False))


@pytest.fixture(scope="module")
def built(pools):
    return small_build(pools)


def test_small_build_structure(built):
    fb, b = built
    tr, dev = fb.rows_for("train"), fb.rows_for("dev")
    assert len(tr) == 2 * SMALL["train"] and len(dev) == 2 * (SMALL["dev_iid"] + SMALL["dev_holdout"])
    units = {}
    for r in tr + dev:
        units.setdefault(r["meta"]["latent_id"], []).append(r)
    for lid, us in units.items():
        assert [u["meta"]["view"] for u in us] == ["base", "ladder"]
        base, lad = us
        assert base["state"] == lad["state"] and base["meta"]["polarity"] == 0 and base["meta"]["role"] == "para"
        assert lad["meta"]["polarity"] in (1, 2) and lad["meta"]["role"] == {1: "neg", 2: "dneg"}[lad["meta"]["polarity"]]
        src = b.sources[lid]
        assert base["gold"] == g._yn(src["truth"])
        assert lad["gold"] == g._yn(pf.gold(src["truth"], src["cell"]))
    rels = {(x["a"], x["b"]): x["type"] for x in fb.rels}
    for lid, (base, lad) in units.items():
        assert rels[(base["rid"], lad["rid"])] == ("complement" if lad["meta"]["polarity"] == 1 else "equiv")
    assert {r["meta"]["dev_kind"] for r in dev} == {"iid", "holdout"}
    for r in dev:   # dev is (b)-type only (R3); holdout dev uses only the held-out frame families
        assert b.sources[r["meta"]["latent_id"]]["kind"] == "b"
        fam = pf.QUAD[r["meta"]["tpl"].split(".")[0]]["family"]
        assert (fam in pf.HOLDOUT_FAMILIES) == (r["meta"]["dev_kind"] == "holdout")


def test_small_build_f4a_provenance(built):
    fb, b = built
    a_rows = [r for r in fb.rows_for("train") if b.sources[r["meta"]["latent_id"]]["kind"] == "a"]
    assert len(a_rows) == SMALL["train"]   # half of the train latents
    for r in a_rows:
        m, src = r["meta"], b.sources[r["meta"]["latent_id"]]
        assert m["derived_from"] == src["base_id"] and m["derived_by"] == g.DERIVED_BY
        assert m["derived_group"] == src["group_id"] and m["dataset"] and m["licence"] and m["revision"]
        assert m["licence"] != mv.LICENCE and m["fmt"] == "prose" and m["pack"] == "a"
        assert src["label"] in (src["gold_label"], *src["bundle"]) and src["gold_label"] in src["bundle"]
        assert src["truth"] == (src["label"] == src["gold_label"])
    golds = Counter(b.sources[r["meta"]["latent_id"]]["truth"] for r in a_rows if r["meta"]["view"] == "base")
    assert abs(golds[True] - golds[False]) <= 2


def test_small_build_cards_and_judge(built):
    fb, b = built
    for r in fb.rows:
        d = fb.defs[r["meta"]["defs"]]
        assert list(d)[-2:] == ["yes", "no"]
        assert ps.A_HOLDS_KEY in d and ps.A_FAILS_KEY in d
        y, n = pf.render(*r["meta"]["tpl"].split("."), b.sources[r["meta"]["latent_id"]]["P"])[1:]
        assert d["yes"] == y and d["no"] == n
        if b.sources[r["meta"]["latent_id"]]["kind"] == "a":
            assert ps.A_TASK_KEY in d and r["meta"]["card_style"] != "none"
        if r["meta"]["judge"]:
            assert pf.is_record(r["meta"]["tpl"].split(".")[0])
            assert not mv.judge_violations(r["instructions"], *d, *d.values())
        assert not JUDGE_RX.search(r["instructions"])


def test_small_build_gates(built):
    """The structural gates hold at any size; the 45-55% strata balance and the +-3 pp tier mix need the full build
    (tiny strata of a 40-latent build cannot all be within one row) and are gated in
    test_gen3_polarity_ladder_written.py."""
    fb, b = built
    for part in ("train", "dev"):
        rows = fb.rows_for(part)
        rids = {r["rid"] for r in rows}
        rep = mv.run_checks(rows, [x for x in fb.rels if x["a"] in rids])
        for k in ("structure", "shortcuts", "plants", "keysets", "none", "positions", "edges"):
            assert rep[k]["ok"], (part, k, json.dumps(rep[k], default=str)[:600])
        assert rep["tiers"]["hard_below_2"] == 0 and rep["tiers"]["hard_without_shortcuts"] == 0
        assert mv.share_ok(sum(r["gold"] == "yes" for r in rows), len(rows))
        for pol in (0, 1, 2):
            xs = [r for r in rows if r["meta"]["polarity"] == pol]
            assert mv.share_ok(sum(r["gold"] == "yes" for r in xs), len(xs)), (part, pol)


def test_small_build_selfcheck(built):
    fb, b = built
    truth = g.truth_from_rows()
    for r in fb.rows:
        assert g.selfcheck_row(r, b.sources[r["meta"]["latent_id"]], truth), r["rid"]


def test_small_build_is_deterministic(pools, built):
    fb2, b2 = small_build(pools)
    assert fb2.rows == built[0].rows and fb2.rels == built[0].rels and b2.sources == built[1].sources


def test_small_build_assembles(built):
    fb, _ = built
    rows, rels = mv.assemble(fb.rows, fb.rels, lambda r: fb.defs.get(r["meta"]["defs"]))
    for r in rows:
        assert r["qtype"] == "noul" and r["options"] is None and r["gold"] in (0, 1)
        assert "teacher" not in r["meta"]
        if r["meta"].get("derived_from"):
            assert r["group_id"].startswith("g:gd:") and r["call_id"] == mv.cid(r["group_id"])
        else:
            assert r["group_id"] == f"g:yn2b:{g.KEY}:{r['meta']['latent_id']}"
    assert len(rels) == len(fb.rels)
