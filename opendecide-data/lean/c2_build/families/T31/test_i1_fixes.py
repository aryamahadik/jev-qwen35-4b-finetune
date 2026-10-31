"""families/T31/test_i1_fixes.py: tests of fix iteration 1 (pilot/PILOT_VERDICT.json F01-F10, P1-P5; G0 v1.2).

  F01 the 20 {cap|ITEM} skins are quarantined (they fail G3)       F02 G3-H item field: no leading article
  F03 Mode F documents with a name / pronoun / claim outside the slot are screened out
  F04 choiceplan: escalate gold 1/k, balanced position and length rank, no twin where escalate is shown
  F05 yes/no twins are about as often yes as no                     F06 the agent yes/no base form is drawn from all four
  F07 double-negation forms: fallback while no wording is admitted; polarity rule; the authoring brief
  F08 equiv share                                                    F09 cards: rules in row.card (yes/no), 3 styles
  F10 the frozen packs and names are wired, one pack per card        P1 register-first, P2 rows per skin, determinism
No Haiku, no model, nothing written. Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T31
"""
from __future__ import annotations

import collections
import dataclasses
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import choiceplan as CP  # noqa: E402
from c2_kit import pipeline  # noqa: E402
from c2_kit import polarity as POL  # noqa: E402
from c2_kit import skin as K  # noqa: E402
from c2_kit.plugin import ContractError  # noqa: E402
from families.T31 import dneg_authoring as DN  # noqa: E402
from families.T31 import fixtures as FX  # noqa: E402
from families.T31 import plugin as P  # noqa: E402

HERE = Path(__file__).resolve().parent
TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def real():
    """(plugin, ctx) over the frozen pools_v2 (what the pilot uses)."""
    from families.T31 import freeze_v2 as FV
    pools = FV.load_pools()
    return P.T31(lexicon=pools["lexicon"]), FV.kit_ctx(pools)


@pytest.fixture(scope="module")
def fx():
    c = FX.ctx()
    return P.T31(lexicon=c.lexicon), c


def _units(plugin, ctx, seeds, samplers=TRAIN, g15=False):
    out = []
    for seed in seeds:
        for smp in samplers:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=g15)
            assert res.ok, (seed, smp, res.problems)
            out.append(res)
    return out


# ------------------------------------------------------------------------------------------------ F10 packs and names

def test_packs_are_the_frozen_pools_and_one_per_card(real):
    plugin, _ = real
    assert len(plugin.pack_by_id) == 70 and len(plugin.names) == 320
    for track in ("appr", "agent"):
        ids = {}
        for smp in P.T31.SAMPLERS:
            for card in range(P.CARDS):
                pid, pack = plugin.pack_for(smp, track, card)
                ids[(smp, card)] = pid
                assert pid.startswith(f"t31:{track}:p") and plugin.pack_by_id[pid] is pack
        assert len(set(ids.values())) == 30                        # 24 training cards + 6 S5 cards, all different
        assert all(ids[("S5", c)] not in {v for (s, _), v in ids.items() if s != "S5"} for c in range(P.CARDS))


def test_a_changed_frozen_pool_is_refused(tmp_path):
    for n in ("packs.json", "MANIFEST.json"):
        (tmp_path / n).write_bytes((P.POOLS_V2 / n).read_bytes())
    P.load_packs(tmp_path)
    (tmp_path / "packs.json").write_bytes((P.POOLS_V2 / "packs.json").read_bytes().replace(b"formulary", b"Formulary", 1))
    with pytest.raises(ContractError):
        P.load_packs(tmp_path)


def test_rows_draw_from_the_pools_and_no_two_people_share_a_name_word(real):
    plugin, _ = real
    names, packs = set(), collections.Counter()
    for seed in range(60):
        for smp in P.T31.SAMPLERS:
            spec = plugin.sample(seed, smp)
            pack = plugin.pack_by_id[spec.pack]
            people = [s.value for k, s in spec.slots.items() if s.kind == "name" and (k.startswith("PERSON_")
                                                                                       or k in ("REQUESTER", "PRINCIPAL"))]
            assert set(people) <= set(plugin.names)
            toks = [t for n in people for t in P._name_tokens(n)]
            assert len(toks) == len(set(toks)), (spec.seed, people)
            names |= set(people)
            packs[spec.pack] += 1
            if spec.structure["track"] == "appr":
                assert {spec.slots[f"ROLE_{i + 1}"].value for i in range(len(spec.structure["matrix"]))} <= set(pack["roles"])
                assert spec.slots["PROCESS"].value == pack["process"] and spec.slots["ITEM"].value in pack["items"]
            else:
                ids = {s.value for s in spec.slots.values() if s.kind == "id"}
                scopes = {spec.slots[x].value for g in spec.structure["grants"] for x in g["scopes"]}
                assert scopes <= set(pack["scopes"]) and spec.slots[spec.structure["chain"][0]].value in pack["agents"], ids
    assert len(names) > 200 and len(packs) >= 48


# ------------------------------------------------------------------------------------------------ F01 / F03 quarantine

def test_the_listed_skins_and_documents_never_reach_a_row(real):
    plugin, ctx = real
    bad = plugin.quarantined(ctx)
    assert P.I1_QUARANTINED_SKINS <= set(bad) and P.I1_QUARANTINED_DOCUMENTS <= set(bad)
    assert len(P.I1_QUARANTINED_SKINS) == 20 and len(P.I1_QUARANTINED_DOCUMENTS) == 12
    assert len(bad) == 38
    used = collections.Counter()
    for u in _units(plugin, ctx, range(40)):
        for r in u.rows:
            used[r["meta"]["c2"]["skin_id"]] += 1
    assert not set(used) & set(bad)
    assert any(r["meta"]["c2"]["author_mode"] == "F" for u in _units(plugin, ctx, range(20)) for r in u.rows)


def test_a_cap_item_skin_fails_g3_which_is_why_it_is_quarantined(real):
    plugin, ctx = real
    sid = sorted(P.I1_QUARANTINED_SKINS)[0]
    sk = ctx.skin(sid)
    assert "{cap|ITEM}" in sk.text
    track = P.skin_track(sk)
    for seed in range(60):
        spec = plugin.sample(seed, "S1")
        if spec.structure["track"] != track:
            continue
        rr = plugin.render(spec, ctx, skin=sk)                       # the raw pool, not ctx_for: the skin is in it
        probs = pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False)
        assert any(g == "G3" and "item" in d for g, d in probs), probs
        return
    pytest.fail("no spec of the skin's track")


def test_freeform_leaks_catch_a_second_name_a_pronoun_and_a_claim():
    brief = (("ITEM", "hotel change"), ("REQUESTER", "Ines Duarte"), ("REQ_ID", "TASK-4535"))
    ok = "This message comes from Ines Duarte. Please take care of the hotel change under reference TASK-4535."
    assert P.freeform_leaks(ok, brief) == [] and P.claim_phrases(ok) == []
    assert P.freeform_leaks(ok + " Ines appreciates the careful attention.", brief) == [
        "name word 'ines' outside the REQUESTER value"]
    assert any("duarte" in x for x in P.freeform_leaks(ok + " Mr Duarte is away.", brief))
    assert any("pronoun" in x for x in P.freeform_leaks(ok + " She wants it done carefully.", brief))
    assert P.claim_phrases("Thanks, the setup looks good.") == ["claim phrase 'looks good'", "claim phrase 'setup looks'"]
    assert P.freeform_leaks("Pieter de Vries asks about the hotel change.", (("REQUESTER", "Pieter de Vries"),)) == []


def test_render_refuses_a_document_that_leaks_even_without_ctx_for(fx):
    plugin, ctx = fx
    doc = K.make_skin("T31-X-F", "T31", "Mara Quist here. Mara asks for a decision on the fleet lease under REQ-1001.",
                      {"REQUESTER": "name", "ITEM": "name", "REQ_ID": "id"}, register="email", author_mode="F",
                      brief={"REQUESTER": "Mara Quist", "ITEM": "fleet lease", "REQ_ID": "REQ-1001"},
                      haiku_task_id="t", haiku_prompt_sha="0" * 64)
    with pytest.raises(K.RenderError):
        plugin.render(plugin.sample(3, "S1"), ctx, skin=doc)


# ------------------------------------------------------------------------------------------------ F02

def test_extract_fields_item_asks_for_the_noun_phrase_without_its_article(fx):
    plugin, _ = fx
    f = {x.name: x for x in plugin.extract_fields(plugin.sample(1, "S1"))}
    assert "without a leading article" in f["item"].describe and "the, a, an" in f["item"].describe


# ------------------------------------------------------------------------------------------------ F04 choice plan

def test_choice_plans_are_label_blind_balanced_and_met(fx):
    plugin, ctx = fx
    pos, rank, cells = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter), {}
    for seed in range(0, 480):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if spec.qform not in ("ch_approver", "ch_scope"):
                continue
            plan = plugin._plan(spec)
            assert plan == plugin._plan(dataclasses.replace(spec, structure=spec.structure))           # row key only
            assert plan.accepts(plugin.solve_a(spec), P.ESCALATE if spec.qform == "ch_approver" else None)
            assert plan.k in P.CHOICE_KS and (spec.qform == "ch_approver" or not plan.show_abstain)
            pos[(spec.qform, plan.k)][plan.pos] += 1
            if plan.rank is not None:
                rank[(spec.qform, plan.n_ordered)][plan.rank] += 1
            c = cells.setdefault((plan.k, plan.show_abstain), [0, 0]) if spec.qform == "ch_approver" else [0, 0]
            c[0] += 1
            c[1] += plan.gold_abstain
    for table in (pos, rank):
        for key, counts in table.items():
            n = sum(counts.values())
            if n >= 30:
                assert max(counts.values()) - min(counts.get(i, 0) for i in range(max(counts) + 1)) <= 0.45 * n / len(counts) + 4, (key, counts)
                assert CP.chi2_uniform_p([counts.get(i, 0) for i in range(len(counts))]) > 0.05, (key, counts)
    for (k, shown), (n, ab) in cells.items():
        assert shown or ab == 0
        if shown and n >= 40:
            assert CP.binom_two_sided(ab, n, 1 / k) > 0.001, (k, ab, n)
    assert abs(sum(n for (k, sh), (n, _) in cells.items() if sh) / sum(n for n, _ in cells.values()) - P.APPR_ABSTAIN_SHOW) < 0.04


def test_emitted_option_sets_meet_the_plan(fx):
    plugin, ctx = fx
    sets, roles = [], []
    for u in _units(plugin, ctx, range(300)):
        for rr in u.rendered:
            if rr.option_set is not None:
                sets.append(rr.option_set)
                roles.append(rr.row["role"])
                if rr.row["role"] == "twin":
                    assert not rr.option_set.abstain_shown and rr.row["meta"]["qform"] == "ch_approver"
    rep = CP.plan_report(sets, longest_pp=4.0)
    cells = {k: v for k, v in rep["abstain_cells"].items() if "shown=True" in k}
    assert cells and all(v["share"] <= 0.5 for v in cells.values()), cells
    for k, v in cells.items():
        if v["rows"] >= 40:
            assert v["p_binom"] > 0.001, (k, v)
    assert rep["longest_gold_pp"] is not None and abs(rep["longest_gold_pp"]) <= 4.0, rep["longest_gold_pp"]
    assert all(p is None or p > 0.001 for p in rep["positions_chi2_p"].values()), rep["positions_chi2_p"]


def test_a_twin_exists_only_where_the_escalate_option_is_not_shown(fx):
    plugin, _ = fx
    seen = collections.Counter()
    for seed in range(200):
        spec = plugin.sample(seed, "S1")
        if spec.qform != "ch_approver":
            continue
        has = any(p.kind == "twin" for p in plugin.relations(spec))
        seen[(plugin._plan(spec).show_abstain, has)] += 1
    assert seen[(True, True)] == 0 and seen[(False, True)] > 10 and seen[(True, False)] > 5, seen


# ------------------------------------------------------------------------------------------------ F05, F06, F08

def test_twins_are_about_as_often_yes_as_no_and_agent_forms_are_balanced(fx):
    plugin, ctx = fx
    yn_twin, bad = collections.Counter(), collections.Counter()
    base_forms = collections.Counter()
    for u in _units(plugin, ctx, range(260)):
        for r in u.rows:
            q = plugin.QFORMS[r["meta"]["qform"]]
            if r["qtype"] == "noul" and r["role"] == "twin":
                yn_twin[r["gold"]] += 1
            if r["qtype"] == "noul" and q.yes_is_bad is not None:
                bad[q.yes_is_bad] += 1
            if r["role"] == "base":
                base_forms[r["meta"]["qform"]] += 1
    assert yn_twin[1] / sum(yn_twin.values()) == pytest.approx(0.5, abs=0.08), yn_twin
    assert bad[True] / sum(bad.values()) == pytest.approx(0.5, abs=0.06), bad
    assert all(base_forms[q] > 20 for q in ("yn_agent_ok", "yn_agent_beyond", "yn_agent_lacks", "yn_agent_not"))
    for q in ("yn_agent_beyond", "yn_agent_lacks", "yn_agent_not"):
        assert P.COMPLEMENTS[q] == (("yn_agent_ok", 1.0),)


def test_equiv_and_attack_shares(fx):
    plugin, ctx = fx
    rows = [r for u in _units(plugin, ctx, range(260)) for r in u.rows]
    n = len(rows)
    assert 0.05 <= sum(r["role"] == "equiv" for r in rows) / n <= 0.10
    assert 0.03 <= sum(r["role"] == "attack" for r in rows) / n <= 0.08


# ------------------------------------------------------------------------------------------------ F07

def test_double_negation_forms_fall_back_until_a_clean_wording_is_admitted():
    c0 = FX.ctx(dneg=False)
    p0 = P.T31(lexicon=c0.lexicon)
    assert p0.dneg_ok == {"yn_holder_dneg": False, "yn_agent_dneg": False}
    forms = collections.Counter(p0.sample(s, smp).qform for s in range(300) for smp in TRAIN)
    assert not {"yn_holder_dneg", "yn_agent_dneg"} & set(forms)
    assert forms["yn_holder"] > 0 and forms["yn_agent_ok"] > 0
    c1 = FX.ctx()
    p1 = P.T31(lexicon=c1.lexicon)
    assert p1.dneg_ok == {"yn_holder_dneg": True, "yn_agent_dneg": True}
    forms = collections.Counter(p1.sample(s, smp).qform for s in range(300) for smp in TRAIN)
    assert 0.05 < forms["yn_holder_dneg"] / sum(forms.values()) < 0.12 and forms["yn_agent_dneg"] > 30


def test_double_negation_rows_pass_every_gate_with_two_negations_and_a_syntactic_partner(fx):
    plugin, ctx = fx
    seen, partners = collections.Counter(), collections.Counter()
    for u in _units(plugin, ctx, range(260), g15=False):
        for r in u.rows:
            if r["meta"]["qform"] in ("yn_holder_dneg", "yn_agent_dneg"):
                seen[r["role"]] += 1
            if r["role"] == "complement":
                partners[r["meta"]["qform"]] += 1
    assert seen["base"] > 10 and partners["yn_holder_not"] > 0 and partners["yn_agent_not"] > 0
    import negcount
    for wid, qf, text, _ in FX.WORDINGS:
        if qf.endswith("dneg"):
            c = negcount.count(K.PH_RE.sub("X", text))
            assert (c.k_syn, c.k_all) == (2, 2) and POL.form_problems(P.T31, qf, text) == []


def test_polarity_rule_screens_the_frozen_pool_and_a_wrong_wording(real, fx):
    plugin, ctx = real
    bad = {k: v for k, v in plugin.quarantined(ctx).items() if v and v[0].startswith(("P1", "P2", "P3", "P4"))}
    assert len(bad) == 1 and "too much" in ctx.skin(next(iter(bad))).text          # the one frozen wording that reads either way
    wordings = [s for s in ctx.skins.values() if s.kind == "wording"]
    assert len(wordings) == 180 and sum(bool(POL.form_problems(P.T31, s.qform, s.text)) for s in wordings) == 1
    plugin2, ctx2 = fx
    wrong = K.make_skin("T31-W-WRONG", "T31", "Is it not the case that {CANDIDATE} did not block the accountable approver?",
                        {"CANDIDATE": "name"}, kind="wording", register="question", qform="yn_holder_dneg")
    c3 = dataclasses.replace(ctx2, skins={**ctx2.skins, wrong.skin_id: wrong})
    assert "T31-W-WRONG" in plugin2.quarantined(c3) and "T31-W-WRONG" not in plugin2.ctx_for(plugin2.sample(1, "S1"), c3).skins
    assert POL.form_problems(P.T31, "yn_holder_dneg", wrong.text)[0].startswith("P1")


def test_dneg_authoring_brief_and_admission_check():
    good = {"yn_holder_dneg": "Is it not the case that {CANDIDATE} was not the accountable approver when the request was made?",
            "yn_agent_dneg": "Is it not true that {REQ_AGENT} is not permitted to use {REQ_SCOPE} at the time of the request?"}
    for q, t in good.items():
        assert DN.wording_problems(q, t) == [], (q, DN.wording_problems(q, t))
    bad = [("yn_holder_dneg", "Is it not the case that {CANDIDATE} did not block the accountable approver role?", "P1"),
           ("yn_holder_dneg", "Isn't it the case that {CANDIDATE} was not the accountable approver?", "P3"),
           ("yn_holder_dneg", "Is it not the case that {CANDIDATE} was the accountable approver?", "k_syn 1"),
           ("yn_agent_dneg", "Is it not the case that {REQ_AGENT} is not barred from using {REQ_SCOPE} at that moment?", "P1"),
           ("yn_agent_dneg", "Is {REQ_AGENT} not unable to use {REQ_SCOPE} at that moment?", "outer frame"),
           ("yn_holder_dneg", "Is it not the case that {CANDIDATE} was not the one who may escalate this?", "abstain")]
    for q, t, why in bad:
        probs = DN.wording_problems(q, t)
        assert any(why in p for p in probs), (t, probs)
    batches = DN.build_batches()
    assert len(batches) == 2 and all(len(b.chunks[0]["items"]) == DN.PER_FORM for _, b in batches)
    assert "exactly two" in DN.prompt("appr") or "two cancelling" in DN.prompt("appr")


# ------------------------------------------------------------------------------------------------ F09 cards

def test_yes_no_rows_print_the_rules_once_in_the_card_and_choice_rows_keep_them_in_the_instructions(fx):
    plugin, ctx = fx
    n = collections.Counter()
    for u in _units(plugin, ctx, range(120), g15=False):
        for rr in u.rendered:
            r, spec = rr.row, None
            style = r["meta"]["defs_style"]
            assert re.fullmatch(r"rules_in_(card|instructions)_(full|compact|short)", style), style
            if r["qtype"] == "noul":
                assert r["card"] and style.startswith("rules_in_card") and "\n\n" not in r["instructions"]
                assert r["card"].endswith(P.CLOSED_WORLD) and r["instructions"].endswith("?")
                n["yn"] += 1
            else:
                assert r["card"] is None and style.startswith("rules_in_instructions")
                rules, q = r["instructions"].rsplit("\n\n", 1)
                assert rules.endswith(P.CLOSED_WORLD) and q.endswith("?")
                n["ch"] += 1
            n[style.rsplit("_", 1)[1]] += 1
    assert n["yn"] > 200 and n["ch"] > 200 and n["full"] > 0 and n["compact"] > n["full"] and 0 < n["short"] < 0.25 * (
        n["yn"] + n["ch"])


def test_a_twin_a_complement_and_an_equiv_partner_share_the_card_style(fx):
    plugin, ctx = fx
    for u in _units(plugin, ctx, range(80)):
        assert len({r["meta"]["defs_style"].rsplit("_", 1)[1] for r in u.rows}) == 1


def test_solver_b_reads_every_card_style_in_both_layouts(fx):
    plugin, ctx = fx
    seen = set()
    for seed in range(160):
        spec = plugin.sample(seed, TRAIN[seed % 4])
        rr = plugin.render(spec, ctx)
        view = plugin.parse(rr.row, ctx)
        assert plugin.solve_b(view) == rr.answer
        seen.add((rr.row["qtype"], rr.row["meta"]["defs_style"]))
    assert len(seen) >= 6


def test_the_card_is_the_one_in_g0_v12():
    g0 = " ".join((HERE / "G0_SPEC.md").read_text(encoding="utf-8").split())
    assert " ".join(P.CARD_TEXT["appr"]["full"].split()) in g0
    assert hashlib.sha256((HERE / "G0_SPEC_v1_1.md").read_bytes()).hexdigest() == P.POOL_G0_SHA256
    assert hashlib.sha256((HERE / "G0_SPEC.md").read_bytes()).hexdigest() == P.T31.G0_SHA256 != P.POOL_G0_SHA256


# ------------------------------------------------------------------------------------------------ P1, P2, determinism

def test_register_first_pick_and_the_skin_row_cap(real):
    plugin, ctx = real
    units = _units(plugin, ctx, range(70))
    rows = [r for u in units for r in u.rows]
    reg = collections.Counter(r["meta"]["c2"]["register"] for r in rows)
    assert len(reg) == 8 and max(reg.values()) / len(rows) <= 0.16, reg
    per_skin = collections.Counter(r["meta"]["c2"]["skin_id"] for r in rows)
    assert max(per_skin.values()) <= P.SKIN_ROW_CAP and plugin.cap_overflow == 0, (max(per_skin.values()), plugin.cap_overflow)
    ff = sum(r["meta"]["c2"]["author_mode"] == "F" for r in rows) / len(rows)
    assert 0.05 < ff <= 0.25


def test_rows_are_identical_under_two_hash_seeds():
    code = (
        "import sys, json, hashlib\n"
        f"sys.path.insert(0, {str(C2_BUILD)!r})\n"
        "from c2_kit import pipeline\n"
        "from families.T31 import fixtures as FX, plugin as P\n"
        "c = FX.ctx(); pl = P.T31(lexicon=c.lexicon); h = hashlib.sha256()\n"
        "for seed in range(40):\n"
        "    for smp in ('S1', 'S2', 'S3', 'S4'):\n"
        "        res = pipeline.build_unit(pl, pl.sample(seed, smp), c, run_g15=False)\n"
        "        h.update(json.dumps(res.rows, sort_keys=True).encode())\n"
        "print(h.hexdigest())\n")
    out = []
    for hs in ("1", "4242"):
        env = {**os.environ, "PYTHONHASHSEED": hs, "PYTHONDONTWRITEBYTECODE": "1"}
        out.append(subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env, check=True,
                                  cwd=str(C2_BUILD)).stdout.strip())
    assert out[0] == out[1] and len(out[0]) == 64


# ------------------------------------------------------------------------------------------------ F04 b: shape matching

def test_rows_that_show_escalate_have_the_escalate_like_shape_whatever_their_gold(fx):
    """G6 d_meta read the gold off the record counts of the rows that show the escalate option (+16 pp on those rows):
    every such row now has one of two shapes, drawn per seed, and the shape does not depend on the gold."""
    from scipy.stats import fisher_exact
    plugin, _ = fx
    table = collections.Counter()
    for seed in range(0, 700):
        for smp in TRAIN:
            spec = plugin.sample(seed, smp)
            if spec.qform != "ch_approver":
                continue
            plan, st = plugin._plan(spec), spec.structure
            shape = (len(st["delegations"]), len(st["notices"]))
            if not plan.show_abstain:
                continue
            assert shape in ((2, 1), (1, 2)), (seed, smp, shape)
            if shape == (1, 2):
                assert all(n["kind"] == "override" for n in st["notices"])
            table[(plan.gold_abstain, shape)] += 1
    a, b = table[(True, (2, 1))], table[(True, (1, 2))]
    c, d = table[(False, (2, 1))], table[(False, (1, 2))]
    assert min(a, b, c, d) > 10, table                               # both kinds of tie occur, both shapes of decoy
    assert fisher_exact([[a, b], [c, d]])[1] > 0.01, table
    assert abs((b + d) / (a + b + c + d) - P.P_SHAPE_B) < 0.08, table
