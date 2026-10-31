"""families/T31/test_plugin.py: in-memory tests for the T31 plugin (A37 f: nothing is written; no Haiku, no network).

  contract        validate_plugin(strict) == [], solver-B independence, G0-lite frozen and <= 200 lines
  G2 / G3         solver A == solver B and parse == canonical on 5,000 sampled specs (+ every complement form)
  pipeline        every kit program gate (G2, G3, G4, G-SL, G-LEX, G-TW, schema; G15 on a slice) on 750 units,
                  and the spec 4.1 overlay shares
  relations       twins differ in exactly one input slot and the gold moves as constructed; complements opposite;
                  G4 metamorphic predictions hold
  balance         gold labels inside the G0 section 4 bands on 2,000 specs; trap shares; gold positions
  G-SL            the built-in placeholder skins, wordings and attack lines lint clean; no literal value or
                  gold-label word outside the slots of any rendered row
  determinism     same seed -> same spec and rows
  injected bugs   G2, G3 and G-TW catch a broken solver B, solver A, renderer and twin prediction
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T31
"""
from __future__ import annotations

import collections
import dataclasses
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
from c2_kit.distractors import abstain_report  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T31 import fixtures as FX  # noqa: E402
from families.T31 import plugin as P  # noqa: E402
from families.T31 import solver_b as B  # noqa: E402

SAMPLERS = P.T31.SAMPLERS
TRAINING = tuple(s for s in SAMPLERS if s not in P.T31.HELD_OUT_SAMPLERS)
COMPLEMENT_FORMS = {q: tuple(x for x, _ in c) for q, c in P.COMPLEMENTS.items()}   # base form -> its partner forms
BASE_FORMS = tuple(q for q, _ in P.BASE_SHARES)
TOKENIZER = Path(os.path.expanduser("~/.cache/huggingface/hub/models--Qwen--Qwen3.5-4B/snapshots/"
                                    "851bf6e806efd8d0a36b00ddf55e13ccb7b8cd0a/tokenizer.json"))


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T31(lexicon=ctx.lexicon)


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
    assert plugin.PARADIGM_A != plugin.PARADIGM_B
    g0 = Path(plugin.G0_LITE)
    assert len(g0.read_text(encoding="utf-8").splitlines()) <= 200
    assert hashlib.sha256(g0.read_bytes()).hexdigest() == plugin.G0_SHA256


def test_solver_b_shares_no_code_with_solver_a():
    src = Path(B.__file__).read_text(encoding="utf-8")
    assert "families.T31.plugin" not in src and "c2_kit.rules" not in src and "glob_a" not in src
    for name in KP.B_FORBIDDEN_NAMES:
        assert not re.search(rf"\b{name}\b", src), name


def test_fixture_lexicon_forms_pass_their_unit_tests(ctx):
    reg = ctx.lexicon
    assert all(f.unit_ok for f in reg.forms.values()), {k: f.unit_problems for k, f in reg.forms.items()
                                                         if not f.unit_ok}
    assert reg.gate()["pass"]


# ------------------------------------------------------------------------------------------------ G2 / G3

def test_solver_a_equals_solver_b_on_5000_specs(plugin, ctx):
    seen, bases = collections.Counter(), collections.Counter()
    for seed in range(1000):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            _check_row(plugin, ctx, spec, rr)
            seen[spec.qform] += 1
            bases[spec.qform] += 1
            for q2 in COMPLEMENT_FORMS.get(spec.qform, ()):
                s2 = spec.replace(qform=q2)
                r2 = plugin.render(s2, ctx, skin=ctx.skin(rr.skin_id), forms=rr.forms)
                _check_row(plugin, ctx, s2, r2)
                assert r2.answer == 1 - rr.answer
                seen[q2] += 1
    assert sum(bases.values()) == 5000 and set(bases) == set(BASE_FORMS), bases
    assert set(seen) == set(plugin.QFORMS) and min(seen.values()) > 150, seen


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
    assert 0.05 <= rep["equiv_share"] <= 0.10 and 0.03 <= rep["attack_share"] <= 0.08, rep
    assert rep["abstain"]["pass"] and rep["abstain"]["wrong_share"] >= 0.5, rep
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
                if spec.qform != "ch_approver":
                    assert got in (0, 1)
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
    # every twin kind of G0 section 6 occurs: revocation / override times, window ends, bands, chain scopes
    assert {"revoked", "issued", "not_ended", "band", "has", "srev"} <= set(twins), twins
    assert comps > 300 and meta >= 3 * len(specs)


def test_twins_change_one_slot_in_the_rendered_text(plugin, ctx):
    """G-TW on the text: outside the changed slot (and its bracket restatement) the twin row is identical."""
    checked = 0
    for seed in range(120):
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
            checked += 1
    assert checked > 30


# ------------------------------------------------------------------------------------------------ balance

def test_gold_balance_on_2000_specs(plugin, specs):
    yes = collections.defaultdict(list)
    tiers, depth = collections.Counter(), collections.Counter()
    for spec in specs:
        gold = plugin.solve_a(spec)
        depth[spec.deep] += 1
        if spec.qform in BASE_FORMS and spec.qform not in ("ch_approver", "ch_scope"):
            yes[spec.qform].append(gold)
        elif spec.qform == "ch_approver":
            tiers[P._decide(plugin._appr_status(spec))[0]] += 1
    for q, golds in yes.items():                                  # exact by seed pairs (G0 section 4)
        assert abs(sum(golds) / len(golds) - 0.5) <= 0.03, (q, sum(golds), len(golds))
    n = sum(tiers.values())
    # G0 v1.2 section 4: escalate is shown on 40% of the rows and gold on 1/k of those (k 3 or 4): about 11.7% of the
    # ch_approver BASE specs, about 7.5% of all ch_approver rows once twins (none where escalate is shown) are counted
    assert 0.09 <= tiers["escalate"] / n <= 0.15, tiers
    for t in ("override", "delegation", "default"):
        assert 0.22 <= tiers[t] / n <= 0.42, tiers
    assert depth[True] / len(specs) <= 0.10
    qf = collections.Counter(s.qform for s in specs)
    assert 0.40 <= sum(v for q, v in qf.items() if q.startswith("yn_")) / len(specs) <= 0.50, qf
    assert abs((qf["ch_approver"] + sum(v for q, v in qf.items() if q.startswith("yn_holder"))) / len(specs)
               - 0.55) <= 0.03, qf                                       # G0 M1: appr 55 / agent 45


def test_trap_shares_on_2000_specs(plugin, specs):
    tags = collections.Counter(t for s in specs for t in s.tags)
    share = {k: v / len(specs) for k, v in tags.items()}
    targets = {"rev_1min": 0.25, "band_edge": 0.20, "sub_broader": 0.20, "lapsed": 0.15, "escalate_like": 0.10}
    for t, want in targets.items():
        assert share.get(t, 0) >= 0.75 * want, (t, share)
    for t in ("inherit_trap", "notice_after", "notice_at", "conversion", "not_started"):
        assert share.get(t, 0) > 0.01, (t, share)
    # G0 v1.2: depth 3 has weight 8% on S1 / S3 only (token mean, F09 D); report-only tag, capped at 10% by M15
    assert share.get("deep_chain", 0) > 0.005, share


def test_options_come_from_named_error_models(plugin, ctx, specs):
    positions = collections.defaultdict(collections.Counter)
    shown = []
    for spec in specs:
        if spec.qform not in ("ch_approver", "ch_scope"):
            continue
        rr = plugin.render(spec, ctx)
        os_ = rr.option_set
        positions[len(os_.options)][os_.gold_index] += 1
        names = set(P.APPR_EM if spec.qform == "ch_approver" else P.SCOPE_EM)
        for o in os_.options:
            if o.role == "error":
                assert o.err and set(o.err) <= names
            else:
                assert o.role in ("gold", "abstain")
        shown.append(os_)
    for k, c in positions.items():
        m = sum(c.values()) / k
        if m >= 50:
            assert all(abs(c[i] - m) <= 0.35 * m for i in range(k)), (k, c)
    rep = abstain_report(shown)
    assert rep["pass"] and rep["wrong_share"] >= 0.5


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
    assert linted == len(ctx.skins) >= 25
    for sk in ctx.skins.values():                                 # skins and attack lines carry no gold label
        if sk.kind in ("skin", "attack"):
            low = sk.text.lower()
            assert not any(w in low for w in plugin.LABEL_WORDS), sk.skin_id


def test_no_literal_value_or_label_outside_slots(plugin, ctx):
    """Every number, date, time, amount, name and id of a rendered row sits inside a slot span; program templates and
    the card carry no digit, month, weekday or gold-label word of their own (the escalate rule names the option)."""
    months = "|".join(S.MONTHS + S.WEEKDAYS)
    label = re.compile(r"\b(?:" + "|".join(re.escape(w) for w in plugin.LABEL_WORDS) + r")\b", re.I)
    for seed in range(150):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx)
            values = {str(s.value) for s in spec.all_slots().values() if s.kind in ("name", "id")}
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
                for v in values:
                    assert not re.search(r"(?<![\w-])" + re.escape(v) + r"(?![\w-])", rest), (v, seed, smp)
            template = plugin.block_template(spec)
            assert not re.search(r"\d", K.PH_RE.sub("", template)) and not label.search(template)
            for style in P.CARD_TEXT[spec.structure["track"]]:
                rules = plugin._rules(spec, style)
                assert not re.search(r"\d", rules) and not re.search(rf"\b(?:{months})\b", rules)


# ------------------------------------------------------------------------------------------------ determinism

def test_sampling_and_rendering_are_deterministic(plugin, ctx):
    for seed in (0, 7, 31, 202):
        for smp in SAMPLERS:
            a, b = plugin.sample(seed, smp), plugin.sample(seed, smp)
            assert a.structure_hash() == b.structure_hash() and a.tags == b.tags
            assert plugin.render(a, ctx).row == plugin.render(b, ctx).row
    p1, p2 = P.T31(lexicon=ctx.lexicon), P.T31(lexicon=ctx.lexicon)
    u1 = pipeline.build_unit(p1, p1.sample(17, "S4"), ctx, run_g15=False).rows
    u2 = pipeline.build_unit(p2, p2.sample(17, "S4"), ctx, run_g15=False).rows
    assert u1 == u2
    hashes = {plugin.sample(seed, "S1").structure_hash() for seed in range(200)}
    assert len(hashes) == 200


def test_nothing_is_written(plugin, ctx, tmp_path):
    here = Path(__file__).resolve().parent
    before = sorted(p.name for p in here.iterdir())
    pipeline.build_unit(plugin, plugin.sample(3, "S1"), ctx, run_g15=False)
    assert sorted(p.name for p in here.iterdir()) == before
    if not paths.a38_frozen():
        with pytest.raises(paths.DataBeforeFreeze):
            paths.write_jsonl(paths.C2_PARTS / "t31_never.jsonl", [])


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
    holder, usable = B._holder, B._usable_set                     # B reads every inclusive end as exclusive
    monkeypatch.setattr(B, "_holder", lambda view: holder(dict(view, end_rule="excl")))
    monkeypatch.setattr(B, "_usable_set", lambda view: usable(dict(view, end_rule="excl")))
    assert _failures(plugin, ctx)["G2"] > 0


def test_g2_catches_a_solver_a_band_bug(plugin, ctx, monkeypatch):
    specs = [plugin.sample(seed, smp) for seed in range(150) for smp in TRAINING]
    specs = [s for s in specs if "band_edge" in s.tags and s.qform == "ch_approver"]
    monkeypatch.setitem(P.CMP_OP, "cmp.le", "<")                  # solver A reads "up to and including" as strict
    g2 = 0
    for s in specs:
        try:
            rr = plugin.render(s, ctx)
        except K.RenderError:                                     # the buggy gold cannot even fill its options
            continue
        g2 += sum(g == "G2" for g, _ in pipeline.check_rendered(plugin, s, rr, ctx, run_g15=False))
    assert g2 > 0
    with pytest.raises(KP.ContractError):                         # and the sampler's own guard refuses it too
        for seed in range(400):
            plugin.sample(seed, "S2")


def test_g2_catches_a_mislabelled_option(plugin, ctx, monkeypatch):
    monkeypatch.setattr(P, "ESCALATE_TEXT", "Escalate: two approvers")   # B no longer reads it back
    f = _failures(plugin, ctx, 80)
    assert f["G2"] + f["G3"] > 0


def test_g3_catches_a_renderer_that_drops_a_band(plugin, ctx, monkeypatch):
    monkeypatch.setattr(P, "_band_text", lambda rec: P.NO_BAND)
    assert _failures(plugin, ctx)["G3"] > 0


def test_gtw_catches_a_wrong_twin_prediction(plugin, ctx, monkeypatch):
    real = P.T31._twin

    def flipped(self, spec):
        t = real(self, spec)
        if t is None or spec.qform == "ch_approver":
            return t
        return dataclasses.replace(t, expect=1 - t.expect)

    monkeypatch.setattr(P.T31, "_twin", flipped)
    assert _failures(plugin, ctx)["G-TW"] > 0


def test_gsl_catches_a_leaky_skin(plugin, ctx):
    leaky = dataclasses.replace(ctx.skin("SK-CHAT-1"), skin_id="SK-LEAK",
                                text=ctx.skin("SK-CHAT-1").text + " Ops already authorised it.")
    c2 = dataclasses.replace(ctx, skins={**ctx.skins, "SK-LEAK": leaky})
    spec = plugin.sample(5, "S1")
    rr = plugin.render(spec, c2, skin=leaky)
    assert any(g == "G-SL" for g, _ in pipeline.check_rendered(plugin, spec, rr, c2, run_g15=False))


# ------------------------------------------------------------------------------------------------ review fix: k cells

def test_option_count_and_abstain_display_carry_no_label():
    """k and the abstain display are drawn once from the row key; a spec the draw cannot fill is resampled, never
    re-tried with a smaller k or with the abstain option forced on (escalate never showed at k = 2). Over all emitted
    rows, in every (k, abstain shown) cell with >= 100 rows the abstain-gold share is within 5 pp of the form's share
    and the abstain option is wrong on >= 50% of the rows that show it."""
    from c2_kit import distractors as DI
    c = FX.ctx()
    pl = P.T31(lexicon=c.lexicon)
    sets = collections.defaultdict(list)
    for seed in range(600):
        for smp in ("S1", "S2", "S3", "S4"):
            spec = pl.sample(seed, smp)
            if spec.qform not in ("ch_approver",):
                continue
            res = pipeline.build_unit(pl, spec, c, run_g15=False)
            for rr in (res.rendered if res.ok else []):
                if rr.option_set is not None:
                    sets[spec.qform].append(rr.option_set)
    assert set(sets) == set(("ch_approver",))
    for q, ss in sets.items():
        cells = DI.abstain_cells(ss)
        shown = [v for (k, sh), v in cells.items() if sh]
        share = sum(v["abstain_gold"] for v in shown) / sum(v["rows"] for v in shown)
        for (k, sh), v in cells.items():
            assert sh or v["abstain_gold"] == 0
            if sh and v["rows"] >= 100:
                assert v["wrong_share"] >= 0.5, (q, k, v)
                assert abs(v["abstain_gold"] / v["rows"] - share) <= 0.05, (q, k, v, share)


# ------------------------------------------------------------------------------------------------ G0 v1.1 (Haiku pass)

def _revocations(spec):
    """(revocation time, target window start) for every revocation of a spec (appr and agent)."""
    v, st = spec.env(), spec.structure
    if st["track"] == "appr":
        return [(v[n["time"]], v[st["delegations"][n["target"]]["start"]]) for n in st["notices"]
                if n["kind"] == "revoke"]
    out = []
    for r in st["revocations"]:
        j = r["grant"] if r["grant"] is not None else st["chain"].index(r["agent"])
        out.append((v[r["time"]], v[st["grants"][j]["start"]]))
    return out


def test_revocations_follow_their_targets_start_and_windows_are_not_empty(plugin, specs):
    """G0 M3 / M6 / M10 (points 4 and 5): every window has end > start, and every revocation is issued after the
    start of the delegation or grant it targets, in base specs and in every twin."""
    n_rev = 0
    for spec in specs:
        cases = [spec] + [plugin.derive(p.spec) for p in plugin.relations(spec) if p.kind == "twin"]
        for s in cases:
            v, st = s.env(), s.structure
            recs = st["delegations"] if st["track"] == "appr" else st["grants"]
            assert all(v[r["end"]] > v[r["start"]] for r in recs), (s.seed, s.sampler)
            for t, start in _revocations(s):
                assert t > start, (s.seed, s.sampler, s.qform)
                n_rev += 1
    assert n_rev > 500


def test_track_tagged_skins_and_attack_lines_stay_on_their_track(plugin, ctx):
    """G0 section 7: a skin or attack line whose id carries a track tag is used only on that track (base, equiv and
    inv partners); untagged skins fit both; an explicit wrong-track skin is refused."""
    extra = {}
    for sid, sk in ctx.skins.items():
        if sk.kind in ("skin", "attack") and sk.author_mode == "T":
            for track in ("appr", "agent"):
                nid = f"T31-{track}-{sk.register}-{sid.lower()}"
                extra[nid] = dataclasses.replace(sk, skin_id=nid)
    c2 = dataclasses.replace(ctx, skins={**ctx.skins, **extra})
    assert P.skin_track(extra[next(iter(extra))]) in ("appr", "agent") and P.skin_track(ctx.skin("SK-MEMO-1")) is None
    seen = collections.Counter()
    for seed in range(80):
        for smp in SAMPLERS:
            spec = plugin.sample(seed, smp)
            res = pipeline.build_unit(plugin, spec, c2, run_g15=False)
            assert res.ok, res.problems
            for rr in res.rendered:
                for sid in (rr.skin_id, rr.attack_id):
                    if sid:
                        tr = P.skin_track(c2.skin(sid))
                        assert tr in (None, spec.structure["track"]), (sid, spec.structure["track"])
                        seen[tr] += 1
    assert seen["appr"] > 50 and seen["agent"] > 50
    spec = next(plugin.sample(s, "S1") for s in range(50) if plugin.sample(s, "S1").structure["track"] == "agent")
    wrong = next(s for s in extra.values() if s.kind == "skin" and P.skin_track(s) == "appr" and not s.held_out)
    with pytest.raises(K.RenderError):
        plugin.render(spec, c2, skin=wrong)


def test_card_defines_covering_and_quotes_the_escalate_option(plugin):
    """G0 1.1 (points 6, 7, 9, 12, 15, 24): every card style defines 'covers' and the deciding level, quotes the option
    text, and says listing order and issuers do not matter; solver B's copy is the same text."""
    for track in ("appr", "agent"):
        for style, text in P.CARD_TEXT[track].items():
            assert "Listing order and who issued" in text and text.endswith(P.CLOSED_WORLD), (track, style)
            assert "valid" not in text and "{END}" in text and "{TIMES}" in text
            if track == "appr":
                assert "covers the request" in text.lower() or "covers it" in text.lower()
                assert f'"{P.ESCALATE_TEXT}"' in text and "first level with a covering record" in text
                assert "accountable (A) role" in text and "approver" in text
            else:
                assert "Each agent holds one grant" in text and "exactly when" in text
    assert "The first level with a covering record decides the approver" in P.APPR_RULES
    assert P.APPR_RULES == P.CARD_TEXT["appr"]["full"] and P.AGENT_RULES == P.CARD_TEXT["agent"]["full"]
    assert B._APPR == P.CARD_TEXT["appr"] and B._AGENT == P.CARD_TEXT["agent"]


def test_card_styles_keep_every_rule_and_fit_the_g0_share():
    """c2_kit.cards: compact and short keep the slots, quoted literals, operator words and negation count of the full
    text; the short share is the 15% of spec 3.0 and the style is a function of (seed, sampler, track) only."""
    from c2_kit import cards as CD
    for track, styles in P.CARD_TEXT.items():
        for style in ("compact", "short"):
            assert CD.variant_problems(styles["full"], styles[style]) == [], (track, style)
    assert abs(sum(P.CARD_STYLES.values()) - 1) < 1e-9 and P.CARD_STYLES["short"] <= CD.SHORT_CAP
    c = collections.Counter(CD.draw_style(f"T31|{seed}|S1|appr", P.CARD_STYLES) for seed in range(6000))
    for style, share in P.CARD_STYLES.items():
        assert abs(c[style] / 6000 - share) < 0.03, c
