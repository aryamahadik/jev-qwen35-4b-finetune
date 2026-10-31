"""In-memory tests for the T28 plugin (A37 f: nothing is written; the fixtures are stand-ins, never a pool).

  contract      validate_plugin(strict) == [], solver-B independence, distinct paradigms
  A == B        5,000 sampled specs (1,000 per sampler): render, parse (G3 facts == canonical_for), solver B ==
                solver A, every option text parses back to its key; the plan (third path) agrees too
  relations     build_unit passes every gate on 500 units; twins differ in exactly one input slot and flip as
                predicted; complements are opposite; overlay shares in the spec 4.1 bands
  balance       2,000 specs: verdict thirds per policy, yes rate, yes = bad, question-form and trap shares,
                gold position
  G-SL          every built-in Mode T skin / wording / attack lints clean (no gold-label word, number, name ...);
                the Mode F stand-in passes the fact-lock; program text holds no digit, "$" or "@" outside slot spans
  determinism   same seed -> same spec, rows and option order
  gates bite    injected bugs in solver B, solver A, the renderer, the twin prediction and a skin are caught
Run (from lean/):  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T28
"""
from __future__ import annotations

import collections
import dataclasses
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import gsl, pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T28 import fixtures as FX  # noqa: E402
from families.T28 import plugin as P  # noqa: E402
from families.T28 import solver_b as B  # noqa: E402
import negcount  # noqa: E402  (c_src/common/negcount.py, put on sys.path by c2_kit.paths)

TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T28Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs5000(plugin):
    return [plugin.sample(seed, smp) for smp in plugin.SAMPLERS for seed in range(1000)]


@pytest.fixture(scope="module")
def units(plugin, ctx):
    out = []
    for seed in range(100):
        for smp in plugin.SAMPLERS:
            out.append((seed, smp, pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=seed < 3)))
    return out


# ------------------------------------------------------------------------------------------------ contract

def test_contract(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert KP.check_independence(plugin) == []
    assert plugin.PARADIGM_A != plugin.PARADIGM_B
    src = Path(B.__file__).read_text()
    assert "families.T28.plugin" not in src and "c2_kit.rules" not in src and "glob_a" not in src


def test_lexicon_fixture_is_admitted_and_unit_tested(ctx):
    reg = ctx.lexicon
    assert all(f.unit_ok for f in reg.forms.values())
    assert reg.gate()["pass"]
    assert all(f.required == 3 for f in reg.forms.values() if f.kind == "precedence")
    for p in P.POLICY_IDS:
        assert sum(1 for f in reg.forms.values() if f.sem_id == P.PREC_SEM[p]) >= 2


def test_lexicon_is_required(ctx):
    with pytest.raises(KP.ContractError):
        P.T28Plugin(lexicon=FX.ctx(admit=False).lexicon).sample(1, "S1")
    with pytest.raises(KP.ContractError):
        P.T28Plugin().sample(1, "S1")


# ------------------------------------------------------------------------------------------------ A == B

def test_solver_a_equals_solver_b_on_5000_specs(plugin, ctx, specs5000):
    assert len(specs5000) == 5000
    seen = collections.Counter()
    for spec in specs5000:
        rr = plugin.render(spec, ctx)
        view = plugin.parse(rr.row, ctx)
        facts = {k: v for k, v in view.items() if k != "options"}
        assert facts == plugin.canonical_for(spec, rr.row["meta"]["c2"]["author_mode"]), (spec.seed, spec.sampler)
        a = plugin.solve_a(spec)
        b = plugin.solve_b(view)
        assert a == b == rr.answer, (spec.seed, spec.sampler, spec.qform, a, b)
        if rr.row["qtype"] == "choice":
            assert view["options"][rr.row["options"].index(rr.row["gold"])] == a
            assert len(set(view["options"])) == len(view["options"])
        assert plugin._predict(spec) in (None, a)          # the plan (third path) agrees wherever it answers
        seen[(spec.qform, spec.structure["policy_style"], spec.structure.get("call_style"))] += 1
    styles = {k[1] for k in seen}
    assert styles == {"list", "yaml", "json", "memo", "statements"}
    assert {k[0] for k in seen} == {"ch_verdict", "ch_rule", "ch_inverted", "yn_allow", "yn_allow_syn", "yn_deny",
                                    "yn_deny_syn", "yn_ask", "yn_mustnot"}


def test_every_skin_and_question_form_round_trips(plugin, ctx):
    """Each built-in skin (Mode T text / JSON / YAML and the Mode F stand-in) and every question form passes G2 / G3
    and the per-row gates, with an attack line or without."""
    skins = [s for s in ctx.skins.values() if s.kind == "skin"]
    forms = sorted(plugin.QFORMS)
    n = 0
    for i, sk in enumerate(skins):
        for j, q in enumerate(forms):
            smp = "S5" if sk.held_out else TRAIN[(i + j) % 4]
            spec = None
            for seed in range(400):
                s = plugin.sample(seed, smp)
                if s.qform == q or (q not in P.QFORM_SLOTS and q in P.COMPLEMENT_PARTNERS.get(s.qform, ())):
                    spec = s.replace(qform=q)
                    break
            assert spec is not None, (sk.skin_id, q)
            held = smp == "S5"
            wd = ctx.pick("T28", "wording", f"x|{i}|{j}", qform=q, held_out=held)
            at = ctx.skin("AT-1") if (i + j) % 3 == 0 else None
            rr = plugin.render(spec, ctx, skin=sk, wording=wd, attack=at)
            probs = pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=(i + j) % 9 == 0)
            assert probs == [], (sk.skin_id, q, probs)
            n += 1
    assert n == len(skins) * len(forms)


# ------------------------------------------------------------------------------------------------ relations

def test_build_unit_passes_every_gate(units, plugin):
    bad = [(seed, smp, u.problems[:3]) for seed, smp, u in units if not u.ok]
    assert bad == []
    rep = pipeline.overlay_report([u for _, _, u in units], plugin)
    assert rep["complement_share_of_yes_no"] >= 0.20
    assert rep["non_syntactic_share_of_pairs"] >= 0.30
    assert 0.17 <= rep["twin_share"] <= 0.27
    assert 0.04 <= rep["equiv_share"] <= 0.10
    assert 0.03 <= rep["attack_share"] <= 0.08
    assert 0.45 <= rep["yes_rate"] <= 0.55
    for _, _, u in units:
        assert len(u.rows) <= 4
        cids = collections.Counter(r["call_id"] for r in u.rows)
        assert max(cids.values()) <= 3
        for r in u.rows:
            assert R.validate_row(r) == []
            assert R.approx_tokens(r) <= R.MAX_TOKENS
            assert r["meta"]["dev_only"] == (r["meta"]["sampler"] == "S5" or r["meta"]["c2"]["register"]
                                             in plugin.HELD_OUT_REGISTERS)


def test_twins_change_one_slot_and_flip_as_predicted(plugin, specs5000):
    n = 0
    kinds = collections.Counter()
    for spec in specs5000[:3000]:
        for prop in plugin.relations(spec):
            if prop.kind != "twin":
                continue
            twin = plugin.derive(prop.spec)
            assert slot_diff(spec, twin) == {prop.changed_slot}
            assert twin.structure == spec.structure and twin.qform == spec.qform
            a, b = plugin.solve_a(spec), plugin.solve_a(twin)
            assert b == prop.expect and a != b, (spec.seed, spec.sampler, prop.changed_slot)
            kinds[re.sub(r"\d+", "#", prop.changed_slot)] += 1
            n += 1
    assert n > 900
    assert kinds["CALL_AMT"] and kinds["CALL_TO"] and kinds["R#_EFF"] and kinds["DEFAULT"] and kinds["PREC"]


def test_complements_are_opposite(plugin, specs5000):
    n = 0
    for spec in specs5000[:3000]:
        for prop in plugin.relations(spec):
            if prop.kind != "complement":
                continue
            q1, q2 = plugin.QFORMS[spec.qform], plugin.QFORMS[prop.qform]
            assert q1.predicate == q2.predicate and q1.polarity == -q2.polarity
            assert plugin.solve_a(spec) + plugin.solve_a(spec.replace(qform=prop.qform)) == 1
            n += 1
    assert n > 300


def test_metamorphic_relations_hold(plugin, specs5000):
    notes = collections.Counter()
    for spec in specs5000[::7]:
        base = plugin.solve_a(spec)
        for prop in plugin.relations(spec):
            if prop.kind != "metamorphic":
                continue
            got = plugin.solve_a(plugin.derive(prop.spec))
            assert got == (base if prop.expect == "same" else prop.expect), (spec.seed, spec.sampler, prop.note)
            notes[prop.note] += 1
    assert len(notes) >= 5 and min(notes.values()) > 20


def test_complement_wordings_have_fixed_negation_counts(ctx, plugin):
    """Complement pairs are checked by cue counts (G-TW), so every wording of a yes/no form must share k_all / k_syn."""
    counts = collections.defaultdict(set)
    for sk in ctx.skins.values():
        if sk.kind == "wording" and plugin.QFORMS[sk.qform].qtype == "noul":
            c = negcount.count(sk.text)
            counts[sk.qform].add((c.k_all, c.k_syn))
    assert all(len(v) == 1 for v in counts.values())
    k = {q: next(iter(v))[0] for q, v in counts.items()}
    for q, partners in P.COMPLEMENT_PARTNERS.items():
        for p2 in partners:
            kind = plugin.QFORMS[p2].complement_kind or plugin.QFORMS[q].complement_kind
            assert abs(k[q] - k[p2]) == (1 if kind == "syntactic" else 0), (q, p2)
    assert k["yn_mustnot_syn"] == 2 and next(iter(counts["yn_mustnot_syn"]))[1] == 2   # double negation


# ------------------------------------------------------------------------------------------------ balance

def test_balance_on_2000_specs(plugin, ctx):
    specs = [plugin.sample(seed, smp) for smp in plugin.SAMPLERS for seed in range(400)]
    assert len(specs) == 2000
    verdict = collections.defaultdict(collections.Counter)
    yes, bad, qf, tags = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    for s in specs:
        a = plugin.solve_a(s)
        qf[s.qform] += 1
        tags.update(s.tags)
        if s.qform == "ch_verdict":
            verdict[s.slots["PREC"].value[0]][a] += 1
        if plugin.QFORMS[s.qform].qtype == "noul":
            yes[a] += 1
            if a == 1:
                bad[bool(plugin.QFORMS[s.qform].yes_is_bad)] += 1
    total = collections.Counter()
    for pol, c in verdict.items():
        n = sum(c.values())
        total.update(c)
        assert all(abs(c[e] / n - 1 / 3) <= 0.025 for e in P.EFFECTS), (pol, c)    # +-2 pp at selection (G10)
    assert len(verdict) == 5
    assert all(abs(total[e] / sum(total.values()) - 1 / 3) <= 0.02 for e in P.EFFECTS)
    assert abs(yes[1] / sum(yes.values()) - 0.5) <= 0.02
    assert abs(bad[True] / sum(bad.values()) - 0.5) <= 0.05
    n = len(specs)
    assert abs(qf["ch_verdict"] / n - 0.40) < 0.01 and abs(qf["ch_rule"] / n - 0.10) < 0.01
    assert abs(qf["ch_inverted"] / n - 0.05) < 0.01
    assert abs(sum(v for k, v in qf.items() if k in P.YN) / n - 0.45) < 0.01
    share = {k: v / n for k, v in tags.items()}
    assert share["first_listed_loses"] >= 0.25
    assert 0.12 <= share["default_decides"] <= 0.19
    assert share["arg_deny_vs_tool_allow"] >= 0.12 and share["amount_at_threshold"] >= 0.12
    assert share["near_miss"] >= 0.08
    p1 = sum(1 for s in specs if s.slots["PREC"].value[0] == "prec.P1")
    assert tags["specific_loses_p1"] / p1 >= 0.20
    assert sum(1 for s in specs if s.deep) / n <= 0.10


def test_gold_position_is_label_blind(plugin, ctx):
    pos = collections.defaultdict(collections.Counter)
    for seed in range(1200):
        spec = plugin.sample(seed, "S1")
        if spec.qform != "ch_verdict":
            continue
        rr = plugin.render(spec, ctx)
        pos[rr.row["meta"]["c2"]["skin_id"]][rr.option_set.gold_index] += 1
        pos["all"][rr.option_set.gold_index] += 1
    c = pos["all"]
    assert all(abs(c[i] / sum(c.values()) - 1 / 3) < 0.06 for i in range(3)), c


def test_wrong_options_name_their_error_models(plugin, ctx):
    names = set(plugin.error_models())
    inverted = 0
    for seed in range(400):
        spec = plugin.sample(seed, TRAIN[seed % 4])
        if spec.qform == "ch_verdict" or spec.qform == "ch_rule" or spec.qform == "ch_inverted":
            rr = plugin.render(spec, ctx)
            errs = rr.row["meta"]["opt_err"]
            assert set().union(*map(set, errs.values())) <= names
            if spec.qform == "ch_inverted":
                assert all(errs.values()), errs                 # every wrong candidate has a named model
                inverted += 1
    assert inverted >= 15


# ------------------------------------------------------------------------------------------------ G-SL

def test_builtin_templates_lint_clean(ctx, plugin):
    checked = 0
    for sk in ctx.skins.values():
        if sk.author_mode != "T":
            continue
        v = gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS,
                              name_allow=plugin.NAME_ALLOW)
        assert v == [], (sk.skin_id, v)
        checked += 1
    assert checked == len(ctx.skins) - 1
    for sk in ctx.skins.values():
        if sk.kind == "skin":
            assert {n for n, _ in sk.slots} == {"USER", "AGENT"}
            low = sk.text.lower()
            assert not any(re.search(rf"\b{re.escape(w)}", low) for w in ("allow", "deny", "ask", "refus", "permit"))


def test_leaky_skins_are_caught(ctx, plugin):
    spec = plugin.sample(5, "S1")
    base = ctx.skin("SK-MEMO-1")
    for extra in (" The admin denied it.", " It is fine to allow.", " Ask first.", " Two calls ran.",
                  " The call came from Bob.", " It was not run."):
        leaky = dataclasses.replace(base, skin_id="SK-LEAK", text=base.text + extra)
        c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK": leaky})
        rr = plugin.render(spec, c2, skin=leaky)
        assert any(g == "G-SL" for g, _ in pipeline.check_rendered(plugin, spec, rr, c2, run_g15=False)), extra


def test_program_text_holds_no_value_outside_slots(plugin, ctx, specs5000):
    """Every digit, amount and address in the state and the card comes from a slot (spans masked); the only
    literal digits are rule ids."""
    for spec in specs5000[::5]:
        rr = plugin.render(spec, ctx)
        for fld in ("state", "instructions"):
            text = rr.row[fld]
            spans = sorted((sp.start, sp.end) for sp in rr.spans if sp.field == fld)
            out, pos = [], 0
            for a, b in spans:
                if a >= pos:
                    out.append(text[pos:a])
                    pos = b
            out.append(text[pos:])
            rest = re.sub(r"\bR\d+\b", "", "".join(out))
            assert not re.search(r"[0-9$@]", rest), (spec.seed, spec.sampler, fld, rest[:400])


# ------------------------------------------------------------------------------------------------ determinism

def test_determinism_by_seed(plugin, ctx):
    other = P.T28Plugin(lexicon=FX.ctx().lexicon)
    for seed in (0, 7, 41, 123, 999):
        for smp in plugin.SAMPLERS:
            a, b = plugin.sample(seed, smp), other.sample(seed, smp)
            assert a.structure_hash() == b.structure_hash() and a.tags == b.tags
            ra = pipeline.build_unit(plugin, a, ctx, run_g15=False).rows
            rb = pipeline.build_unit(other, b, ctx, run_g15=False).rows
            assert ra == rb
    assert plugin.sample(3, "S1").structure_hash() != plugin.sample(3, "S2").structure_hash()
    assert len({plugin.sample(s, "S1").structure_hash() for s in range(300)}) == 300


def test_s5_is_dev_only(plugin, ctx):
    for seed in range(40):
        rows = pipeline.build_unit(plugin, plugin.sample(seed, "S5"), ctx, run_g15=False).rows
        assert rows and all(r["meta"]["dev_only"] for r in rows)
        assert all(R.validate_row(r, training=True) for r in rows)
    held = {p["id"] for p in P.PACKS if p.get("held_out")}
    assert held and all(plugin.sample(s, "S5").pack in held for s in range(60))
    assert not any(plugin.sample(s, smp).pack in held for smp in TRAIN for s in range(60))


# ------------------------------------------------------------------------------------------------ gates bite

def _failures(plugin, ctx, n=40, samplers=("S1", "S3")):
    out = collections.Counter()
    for seed in range(n):
        for smp in samplers:
            res = pipeline.build_unit(plugin, plugin.sample(seed, smp), ctx, run_g15=False)
            out.update(g for g, _ in res.problems)
    return out


def test_g2_catches_a_solver_b_comparator_bug(plugin, ctx, monkeypatch):
    monkeypatch.setitem(B.CMP_SIGNS, "cmp.le", (-1,))                 # "at most" read as strict
    assert _failures(plugin, ctx, 120)["G2"] > 0


def test_g2_catches_a_solver_a_precedence_bug(plugin, ctx, monkeypatch):
    monkeypatch.setitem(P.POLICIES, "P4", "first_match")               # last match evaluated as first match
    assert _failures(plugin, ctx, 200, ("S1",))["G2"] > 0


def test_g3_catches_a_renderer_that_prints_the_wrong_fact(plugin, ctx, monkeypatch):
    monkeypatch.setitem(P.ARG_NAME, "owner", "env")                    # the owner argument printed under "env"
    assert _failures(plugin, ctx, 120)["G3"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = P.T28Plugin._predict

    def flipped(self, spec):                                           # the plan predicts the wrong yes/no answer
        v = real(self, spec)
        return 1 - v if v in (0, 1) and not isinstance(v, bool) else v

    monkeypatch.setattr(P.T28Plugin, "_predict", flipped)
    assert _failures(plugin, ctx, 80)["G-TW"] > 0


# ------------------------------------------------------------------------------- G0 section 9 resolutions

def test_resolved_card_texts_and_rule_shape(plugin, ctx, specs5000):
    """Haiku pass H1-H25: one condition per kind per rule (H8); the literal-character sentence (H3), the closed-world
    sentence without "above" (H42), the owner line exactly when an owner is mentioned (H9-H10), the priority line
    (H25) and the chat call prefix (H11) are printed; no value can make an empty glob run decisive (H1)."""
    n = 0
    for spec in specs5000[::10]:
        env, st = spec.env(), spec.structure
        for r in st["rules"]:
            kinds = [c["kind"] for c in r["conds"]]
            assert len(kinds) == len(set(kinds)) <= 2, (spec.seed, spec.sampler, kinds)
        for k, s in spec.slots.items():
            if k.endswith(("_PATH",)):
                assert "." in s.value.rsplit("/", 1)[1] and not s.value.rsplit("/", 1)[1].startswith(".")
            if k.endswith(("_TO",)):
                assert s.value.split("@", 1)[0] and "." in s.value.split("@", 1)[1]
            if k.endswith("_AMT"):
                assert isinstance(s.value, int) and s.value >= 1
        rr = plugin.render(spec, ctx)
        card = rr.row["instructions"]
        assert P.LITERAL_LINE in card and P.CLOSED_WORLD in card and "above" not in card
        assert (P.OWNER_LINE in card) == plugin._mentions_owner(spec)
        assert (P.PRIORITY_HEAD in card) == (env["PREC"] == "prec.P5")
        if st.get("call_style") == "chat" and st.get("call"):
            assert "\n" + P.CHAT_PREFIX in rr.row["state"]
        n += 1
    assert n == 500
