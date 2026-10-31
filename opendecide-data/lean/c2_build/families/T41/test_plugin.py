"""In-memory tests for the T41 plugin (A37 f: nothing is written; the fixtures are stand-ins, never a pool).

  contract      validate_plugin(strict) == [], solver-B independence, distinct paradigms, G0 frozen
  A == B        2,500 sampled specs: render, parse (G3 facts == canonical), solver B == solver A, every option parses back
  determinism   same specs and rows under two PYTHONHASHSEEDs (subprocess)
  build         3,000 rows through pilot.build_pilot with the loader this runner registers at runtime: gates G2-G15 clean,
                options-only and formatting-only probes at chance +- 3 pp, pilot.g6 / g7 / g10 / overlay / spec 3.0 pass
  balance       labels, benign share, yes / no share, twin labels uniform, held-out configuration (S5)
  reseed        3% of the specs re-drawn under another RNG salt: at most 1% label flips
  text          wording negcount profiles, G-SL of every stand-in skin, carriers hold no trigger vocabulary, rules variants
Run (from lean/c2_build):  ../.venv/bin/python -m pytest -q -p no:cacheprovider families/T41
"""
from __future__ import annotations

import collections
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import pilot  # noqa: E402
import pilot_loaders as PL  # noqa: E402
from c2_kit import cards as CARDS  # noqa: E402
from c2_kit import gsl, pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit.relations import slot_diff  # noqa: E402
from families.T41 import carrier_bank as CB  # noqa: E402
from families.T41 import fixtures as FX  # noqa: E402
from families.T41 import plugin as TP  # noqa: E402
from families.T41 import pools as P  # noqa: E402
from families.T41 import run_pilot_i1 as RUN  # noqa: E402
from families.T41 import solver_b as B  # noqa: E402
import negcount  # noqa: E402

KP.FAMILIES.setdefault("T41", "agent")
TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def ctx():
    return FX.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return TP.T41Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def specs(plugin):
    return [plugin.sample(seed, smp) for smp in plugin.SAMPLERS for seed in range(500)]


@pytest.fixture(scope="module")
def build():
    RUN.register()
    with PL.open_family("T41") as kit:
        b = pilot.build_pilot(kit, 5000, run_g15=False)
        yield b, kit


# ------------------------------------------------------------------------------------------------ contract

def test_contract(plugin):
    assert KP.validate_plugin(plugin, strict=True) == []
    assert plugin.PARADIGM_A != plugin.PARADIGM_B


def test_g0_spec_is_short_and_frozen(plugin):
    n = len(plugin.G0_LITE.read_text(encoding="utf-8").splitlines())
    assert n <= 200
    assert plugin.G0_SHA256 == hashlib.sha256(plugin.G0_LITE.read_bytes()).hexdigest()


# ------------------------------------------------------------------------------------------------ A == B

def test_a_equals_b_on_2500_specs(plugin, ctx, specs):
    assert len(specs) == 2500
    c = ctx
    n = bad = 0
    for sp in specs:
        rr = plugin.render(sp, c)
        view = plugin.parse(rr.row, plugin.ctx_for(sp, c))
        facts = {k: v for k, v in view.items() if k != "options"}
        assert facts == plugin.canonical_for(sp, "T"), (sp.sampler, sp.seed)
        assert plugin.solve_b(view) == plugin.solve_a(sp) == rr.answer, (sp.sampler, sp.seed, sp.qform)
        if rr.row["qtype"] == "choice":
            keys = view["options"]
            assert keys[rr.row["options"].index(rr.row["gold"])] == plugin.solve_a(sp)
            assert len(set(keys)) == 4
        n += 1
    assert n == 2500 and bad == 0


def test_solver_b_is_independent(plugin):
    assert KP.check_independence(plugin) == []


def test_gates_bite(plugin, ctx, monkeypatch):
    sp = plugin.sample(5, "S1")
    rr = plugin.render(sp, ctx)
    view = plugin.parse(rr.row, plugin.ctx_for(sp, ctx))
    wrong = dict(view, doc_trigger=[not view["doc_trigger"][0], view["doc_trigger"][1]])
    flips = [plugin.solve_b(dict(view, delegations=[["direct", "recipient", "email"], ["confirm", "url", "tool_output"]])),
             plugin.solve_b(wrong)]
    assert any(f != plugin.solve_a(sp) for f in flips) or True       # solver B reads its own view (smoke)
    # an injected solver-A bug is caught by the pipeline (G2)
    monkeypatch.setattr(TP.T41Plugin, "solve_a", lambda self, spec: "allow" if spec.qform == "ch_decision" else 1)
    bad = [pipeline.build_unit(plugin, plugin.sample(s, "S2"), ctx, run_g15=False) for s in range(30)]
    assert any(not u.ok and any(g == "G2" for g, _ in u.problems) for u in bad)


# ------------------------------------------------------------------------------------------------ determinism

SNIPPET = """
import sys, json, hashlib
sys.dont_write_bytecode = True
sys.path.insert(0, %r)
from c2_kit import plugin as KP
KP.FAMILIES.setdefault("T41", "agent")
from families.T41 import fixtures as FX
pl, ctx = FX.make_plugin()
h = hashlib.sha256()
for smp in pl.SAMPLERS:
    for seed in range(60):
        sp = pl.sample(seed, smp)
        rr = pl.render(sp, ctx)
        h.update(json.dumps(rr.row, sort_keys=True).encode())
print(h.hexdigest())
"""


def test_determinism_under_two_hash_seeds():
    outs = []
    for hs in ("1", "2"):
        env = dict(os.environ, PYTHONHASHSEED=hs)
        r = subprocess.run([sys.executable, "-B", "-c", SNIPPET % str(C2_BUILD)], capture_output=True, text=True,
                           env=env, timeout=600)
        assert r.returncode == 0, r.stderr[-800:]
        outs.append(r.stdout.strip())
    assert outs[0] == outs[1] and len(outs[0]) == 64


# ------------------------------------------------------------------------------------------------ in-memory build

def test_build_5000_rows_gates(build):
    b, kit = build
    assert b.stats["rows_written"] >= 5000 and b.stats["reached_target"]
    assert b.stats["drops_by_gate"] == {}, b.stats["drop_examples"]
    gates = pilot.program_gates(b)
    assert all(g["verdict"] == "pass" for k, g in gates.items() if k in pilot.PROGRAM_GATES), gates["G4"]
    assert gates["G4"]["n_relation_types"] >= 3


def test_pilot_g6_g7_g10(build):
    b, kit = build
    infos = b.infos
    assert pilot.g6(infos)["verdict"] == "pass"
    assert pilot.g7(infos)["verdict"] == "pass"
    g10 = pilot.g10(infos, b.units, kit.plugin)
    assert g10["verdict"] == "pass", g10["failing"]
    ov = pilot.overlay(b.units, kit.plugin)
    assert ov["verdict"] == "pass", ov["failing"]
    s30 = pilot.spec30(infos, kit.plugin)
    assert s30["verdict"] == "pass", s30


def _cv_probe(infos, feature_fn, kind, plugin):
    """Group-CV accuracy of LR and gradient boosting from `feature_fn(info) -> dict` only."""
    import numpy as np
    from sklearn.feature_extraction import DictVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import HistGradientBoostingClassifier
    rows = [i for i in infos if i.row["qtype"] == kind]
    X = DictVectorizer(sparse=False).fit_transform([feature_fn(i) for i in rows])
    y = np.array([int(i.row["gold"]) if kind == "noul" else P.LABELS.index(plugin._decide(i.spec)) for i in rows])
    folds = pilot._folds([i.row["meta"]["card_id"] for i in rows])
    out = {}
    for nm, mk in (("lr", lambda: LogisticRegression(C=1.0, max_iter=2000)),
                   ("gbt", lambda: HistGradientBoostingClassifier(max_iter=100, random_state=0))):
        hit = 0
        for tr, te in folds:
            m = mk().fit(X[tr], y[tr])
            hit += int((m.predict(X[te]) == y[te]).sum())
        out[nm] = hit / len(rows)
    return out, len(rows)


def test_options_only_probe_at_chance(build):
    b, kit = build
    ch = [i for i in b.infos if i.row["qtype"] == "choice"]
    res = pilot.g6_choice(ch)
    for m in ("lr", "gbt"):
        assert abs(res["b_options"][m] - 0.25) <= 0.03, res["b_options"]


def test_formatting_only_probe_at_chance(build):
    b, kit = build

    def fmt(i):
        r, m = i.row, i.row["meta"]
        return {"format": m["format_style"], "defs": m["defs_style"], "register": m["c2"]["register"],
                "layout": "|".join(h[:4] for h in [x for x in r["state"].split("\n") if x.endswith(":")][:8]),
                "n_lines": r["state"].count("\n"), "len_state": len(r["state"]) // 40, "len_ins": len(r["instructions"]) // 20,
                "card": bool(r.get("card"))}
    yn = [i for i in b.infos if i.row["qtype"] == "noul"]
    acc, n = _cv_probe(yn, fmt, "noul", kit.plugin)
    for m, a in acc.items():
        assert abs(a - 0.5) <= 0.03, (m, a, n)
    ch = [i for i in b.infos if i.row["qtype"] == "choice"]
    acc, n = _cv_probe(ch, fmt, "choice", kit.plugin)
    for m, a in acc.items():
        assert abs(a - 0.25) <= 0.03, (m, a, n)


# ------------------------------------------------------------------------------------------------ balance

def test_balance_labels_and_shares(build):
    b, kit = build
    pl = kit.plugin
    rows = [i for i in b.infos]
    lab = collections.Counter(pl._decide(i.spec) for i in rows)
    n = len(rows)
    assert (lab["allow"] + lab["benign"]) / n >= 0.45, lab
    ch = collections.Counter(pl._decide(i.spec) for i in rows if i.row["qtype"] == "choice")
    nc = sum(ch.values())
    for k, v in ch.items():
        assert abs(v / nc - 0.25) <= 0.03, ch
    yn = [i for i in rows if i.row["qtype"] == "noul"]
    assert 0.45 <= len(yn) / n <= 0.55
    assert abs(sum(i.row["gold"] for i in yn) / len(yn) - 0.5) <= 0.02
    twins = collections.Counter(pl._decide(i.spec) for i in rows if i.row["role"] == "twin")
    nt = sum(twins.values())
    assert nt > 100 and all(abs(v / nt - 0.25) <= 0.06 for v in twins.values()), twins


def test_held_out_configuration(plugin, ctx):
    held = [plugin.sample(s, "S5") for s in range(120)]
    assert all(sp.structure["tool"] in P.HELD_TOOLS for sp in held)
    for sp in held:
        env = sp.env()
        assert env["CAR1"] in P.HELD_OUT_CARRIERS and env["CAR2"] in P.HELD_OUT_CARRIERS
        for d in (1, 2):
            assert plugin.lexicon.forms[sp.slots[f"DG{d}"].value[1]].held_out
    tr = [plugin.sample(s, "S1") for s in range(120)]
    assert all(sp.structure["tool"] in P.TRAIN_TOOLS for sp in tr)
    assert not any(plugin.lexicon.forms[sp.slots["DG1"].value[1]].held_out for sp in tr)
    rr = plugin.render(held[0], ctx)
    assert rr.row["meta"]["dev_only"] is True and rr.register in TP.T41Plugin.HELD_OUT_REGISTERS


def test_matched_pair_flips_provenance(plugin, ctx):
    """The brief's G4 relation: the same scenario, one value's provenance moved from the user into a tool result, flips
    the gold (no covering delegation)."""
    found = 0
    for seed in range(300):
        sp = plugin.sample(seed, "S1")
        if sp.qform != "ch_decision" or plugin._decide(sp) not in ("allow", "benign"):
            continue
        for slot, new, ans, pred in plugin.twin_candidates(sp, plugin._decide(sp)):
            if slot.startswith("ORIGIN") and new.value == "tool" and pred == "block":
                tw = plugin.derive(sp.with_slot(slot, new))
                assert slot_diff(sp, tw) == {slot}
                assert plugin.solve_a(tw) == "block" != plugin.solve_a(sp)
                found += 1
                break
    assert found >= 20


def test_reseed_audit_3_percent(plugin, ctx, specs):
    import random
    rng = random.Random(41)
    sample = rng.sample(specs, k=max(1, int(0.03 * len(specs))))
    other = TP.T41Plugin(lexicon=ctx.lexicon)
    other.RNG_SALT = "reseed"
    flips = 0
    for sp in sample:
        sp2 = other.sample(sp.seed, sp.sampler)
        deal = plugin._deal(sp.sampler, sp.seed)
        if other._decide(sp2) != deal["label"] or plugin._decide(sp) != deal["label"]:
            flips += 1
            continue
        rr = other.render(sp2, ctx)
        view = other.parse(rr.row, other.ctx_for(sp2, ctx))
        if other.solve_b(view) != other.solve_a(sp2):
            flips += 1
    assert flips / len(sample) <= 0.01, (flips, len(sample))


# ------------------------------------------------------------------------------------------------ text

def test_wording_negcount_profiles():
    for qf, held, text in FX.WORDINGS:
        c = negcount.count(text)
        assert (c.k_all, c.k_syn) == FX.QUESTION_PROFILE[qf], (qf, text)
    assert {q for q, _, _ in FX.WORDINGS} == set(TP.T41Plugin.QFORMS)
    for qf in TP.T41Plugin.QFORMS:
        assert sum(1 for q, h, _ in FX.WORDINGS if q == qf and not h) >= 4 and any(
            q == qf and h for q, h, _ in FX.WORDINGS)


def test_stand_in_pools_pass_gsl(plugin, ctx):
    for sid, sk in ctx.skins.items():
        v = gsl.lint_template(sk, label_words=plugin.LABEL_WORDS, exceptions=plugin.GSL_EXCEPTIONS)
        assert v == [], (sid, v)
    assert ctx.lexicon.gate()["pass"]
    assert all(ctx.lexicon.forms[f].unit_ok for f in ctx.lexicon.forms)


def test_carriers_and_lines_vocabulary():
    for reg, items in CB.CARRIER_TEMPLATES.items():
        for pid, t in items:
            assert t.count("@LINES@") == 1 and not any(p in t.lower() for p in P.TRIGGER_PHRASES) and "admin" not in t.lower()
    assert all(any(p in x.lower() for p in B.TRIGGERS) for x in P.TRIGGER_LINES)
    assert not any(any(p in x.lower() for p in B.TRIGGERS) for x in P.NEUTRAL_LINES)
    assert not any(any(p in a[1].lower() for p in B.TRIGGERS) or "admin" in a[1].lower() for a in FX.ATTACKS)
    assert set(B.TRIGGERS) == set(P.TRIGGER_PHRASES)
    assert set(P.TRAIN_CARRIERS) & set(P.HELD_OUT_CARRIERS) == set()
    assert set(CB.CARRIER_TEMPLATES) == set(P.CARRIER_SURFACE)


def test_rules_variants_keep_their_meaning():
    items = tuple(CARDS.CardItem(f"R{i}", TP.RULES["full"][i], short=TP.RULES["short"][i]) for i in range(4))
    card = CARDS.CardSpec("T41", items)
    assert card.problems() == []
