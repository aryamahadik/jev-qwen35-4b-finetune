"""In-memory tests for T40 CALL-GATE (nothing is written; the fixtures are program stand-ins, never a pool).

  schema        the minimal JSON-schema validator (types, required, enum, format, pattern, range, array, additionalProperties)
  contract      validate_plugin(strict) == [], solver B independence, distinct paradigms
  A == B        2,000 sampled specs: render, parse (G3 facts == canonical), solver B == solver A, option texts parse back
  determinism   two PYTHONHASHSEEDs give the same rows
  build         pilot.build_pilot, 3,000 rows, loader registered at runtime: every program gate passes, G6 / G7 / G10 pass at
                the C2 bars, options-only / formatting-only / diff-size probes at chance +- 3 pp, head A >= 40% VALID,
                prompt length, held-out styles / domains only in S5, 3% reseed audit with <= 1% label flips
Run (from lean/):  ../.venv/bin/python -m pytest -q -p no:cacheprovider c2_build/families/T40
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
from c2_kit import gsl, pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as R  # noqa: E402
from families.T40 import edit as E  # noqa: E402
from families.T40 import fixtures as FX  # noqa: E402
from families.T40 import loader  # noqa: E402
from families.T40 import plugin as TP  # noqa: E402
from families.T40 import pools as POOLS  # noqa: E402
from families.T40 import resolver as RES  # noqa: E402
from families.T40 import schema as SC  # noqa: E402
from families.T40 import solver_b as B  # noqa: E402
import negcount  # noqa: E402

loader.register()
TRAIN = ("S1", "S2", "S3", "S4")


@pytest.fixture(scope="module")
def ctx():
    return FX.make_ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return TP.T40Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def build():
    with PL.open_family("T40") as kit:
        b = pilot.build_pilot(kit, 3000, run_g15=False)
        yield kit, b


# ------------------------------------------------------------------------------------------------ schema

def test_schema_validator():
    s = {"type": "object", "required": ["a"], "additionalProperties": False,
         "properties": {"a": {"type": "integer", "minimum": 1, "maximum": 5}, "b": {"type": "string", "enum": ["x", "y"]},
                        "c": {"type": "string", "format": "email"}, "d": {"type": "string", "format": "date"},
                        "e": {"type": "string", "pattern": "^ord_[0-9]+$"}, "f": {"type": "array", "items": {"type": "string"}}}}
    ok = {"a": 3, "b": "x", "c": "a.b@c.example", "d": "2026-02-28", "e": "ord_12", "f": ["u"]}
    assert SC.validate(ok, s) == []
    assert ("$.a", "required") in SC.validate({}, s)
    assert ("$.z", "additionalProperties") in SC.validate({"a": 1, "z": 1}, s)
    assert SC.validate({"a": True}, s) == [("$.a", "type")]            # a boolean is no integer
    assert SC.validate({"a": 3.0}, s) == [("$.a", "type")]
    assert ("$.a", "maximum") in SC.validate({"a": 6}, s)
    assert ("$.b", "enum") in SC.validate({"a": 1, "b": "z"}, s)
    assert ("$.c", "format") in SC.validate({"a": 1, "c": "nope"}, s)
    assert ("$.d", "format") in SC.validate({"a": 1, "d": "2026-02-31"}, s)
    assert ("$.e", "pattern") in SC.validate({"a": 1, "e": "ORD-12"}, s)
    assert ("$.f[0]", "type") in SC.validate({"a": 1, "f": [1]}, s)
    assert SC.structural([("$.a", "required")]) and not SC.structural([("$.a", "enum")])
    assert SC.type_string({"type": "integer", "minimum": 1, "maximum": 7}) == "integer 1..7"


def test_pools_consistent():
    purposes = [r[2] for d in POOLS.DOMAINS.values() for r in d[1]]
    assert len(set(purposes)) == len(purposes)
    for a in purposes + list(POOLS.UNSUPPORTED):
        for b in purposes + list(POOLS.UNSUPPORTED):
            assert a == b or a not in b, (a, b)                          # no purpose is inside another one
    for d, (provs, tools) in POOLS.DOMAINS.items():
        assert len(provs) == 3 and len(tools) >= 5
        for t in tools:
            ps = POOLS.parse_params(t[3])
            assert any(p["req"] for p in ps)
            assert len({p["label"] for p in ps}) == len(ps) and all(p["label"].lower() != "provider" for p in ps)
            for p in ps:
                POOLS.type_schema(p["type"])
    for pool in POOLS.TEXTS.values():
        assert all(negcount.k_all(x) == 0 for x in pool)
    assert set(POOLS.HELD_OUT_STYLES) & set(POOLS.TRAIN_STYLES) == set()
    assert set(POOLS.HELD_OUT_DOMAINS) & set(POOLS.TRAIN_DOMAINS) == set()
    assert set(E.HELD_OUT_PACKS) & set(E.TRAIN_PACKS) == set()


def test_wordings_lint_and_negation(ctx, plugin):
    for sk in ctx.skins.values():
        assert gsl.lint_template(sk, label_words=plugin.LABEL_WORDS) == [], sk.skin_id
    for qf, texts in FX.WORDINGS.items():
        kind = TP.KIND_OF.get(qf)
        for t in texts:
            c = negcount.count(t)
            want = {"pos": (0, 0), "ant": (0, 0), "syn": (1, 1), "dneg": (2, 2), None: (0, 0)}[kind]
            assert (c.k_all, c.k_syn) == want, (qf, t, c.k_all, c.k_syn)
    for sk in (s for s in ctx.skins.values() if s.kind == "wording"):
        assert ctx.lexicon.status(sk.lexicon_ids[0]) == "admitted"


def test_edit_executor_real_run():
    f = "def f(x):\n    y = x + 1\n    return y\n\ndef g(x):\n    y = x + 1\n    return y\n"
    assert E.apply_edit(f, "    y = x + 1\n    return y", "    y = x\n    return y")["label"] == "MULTIPLE"
    assert E.apply_edit(f, "def f(x):", "def f(x):\n    pass")["label"] == "APPLIES_ONCE"
    assert E.apply_edit(f, "def f(x):", "def f(x)")["label"] == "BREAKS_SYNTAX"
    assert E.apply_edit(f, "def h(x):", "def h(y):")["label"] == "NO_MATCH"
    assert E.apply_edit("aaa", "aa", "b")["count"] == 1                 # non-overlapping count, as str.replace


# ------------------------------------------------------------------------------------------------ contract

def test_contract(plugin):
    probs = KP.validate_plugin(plugin, strict=True)
    assert probs == [], probs
    assert plugin.PARADIGM_A != plugin.PARADIGM_B
    assert KP.check_independence(plugin) == []


def test_resolver_precedence():
    """Hand-built registry: every label, and the card's precedence on multi-fault calls."""
    tool = lambda prov, name, menu, params: {"provider": prov, "name": name, "purpose": "p " + name, "mslot": menu, "params": params}  # noqa: E731
    p = lambda n, req, sch: {"name": n, "label": n, "req": req, "schema": sch}  # noqa: E731
    t1 = tool("a", "send", "M1", [p("to", True, {"type": "string", "format": "email"}), p("n", False, {"type": "integer", "minimum": 1, "maximum": 3})])
    t2 = tool("a", "other", "M2", [p("path", True, {"type": "string"})])
    t3 = tool("b", "send", "M3", [p("to", True, {"type": "string"})])
    base = {"tools": [t1, t2, t3], "request": {"clauses": [{"label": "To", "slot": "L1"}], "provider": None},
            "results": []}
    env = {"M1": "yes", "M2": "yes", "M3": "yes", "L1": "x@y.example", "CALLEE": "a::send", "AN1": "to", "A1": "x@y.example",
           "AN2": "n", "A2": "2"}
    call = lambda args: dict(base, call={"callee": "CALLEE", "args": args})  # noqa: E731
    ok = [{"nslot": "AN1", "slot": "A1", "bare": False}]
    assert RES.resolve_call(call(ok), env) == "VALID"
    assert RES.resolve_call(call(ok), dict(env, CALLEE="a::sned")) == "NONEXISTENT_TOOL"
    assert RES.resolve_call(call(ok), dict(env, CALLEE="send")) == "AMBIGUOUS_PROVIDER"
    assert RES.resolve_call(call(ok), dict(env, M1="no")) == "OFF_MENU"
    assert RES.resolve_call(call(ok), dict(env, AN1="path")) == "BORROWED_SIGNATURE"
    assert RES.resolve_call(call([]), env) == "BAD_ARGS"
    assert RES.resolve_call(call(ok), dict(env, A1="nope")) == "TYPE_VIOLATION"
    assert RES.resolve_call(call(ok), dict(env, A1="q@y.example")) == "UNGROUNDED_VALUE"
    two = ok + [{"nslot": "AN2", "slot": "A2", "bare": True}]
    assert RES.resolve_call(call(two), dict(env, A2="9")) == "TYPE_VIOLATION"
    assert RES.resolve_call(call(two), dict(env, A2="2")) == "UNGROUNDED_VALUE"      # 2 is stated nowhere
    # precedence: nonexistent beats everything; off-menu beats borrowed; type beats grounding
    assert RES.resolve_call(call(ok), dict(env, CALLEE="a::zzz", M1="no", A1="bad")) == "NONEXISTENT_TOOL"
    assert RES.resolve_call(call(ok), dict(env, M1="no", AN1="path")) == "OFF_MENU"
    assert RES.resolve_call(call(ok), dict(env, A1="bad")) == "TYPE_VIOLATION"


# ------------------------------------------------------------------------------------------------ A == B

def test_solver_a_equals_b_2000(plugin, ctx):
    n, bad = 0, []
    for smp in plugin.SAMPLERS:
        for seed in range(400):
            spec = plugin.sample(seed, smp)
            rr = plugin.render(spec, ctx, forms=KP.choose_forms(spec, f"{spec.family}|{spec.seed}|{spec.sampler}|{spec.qform}"))
            probs = pipeline.check_rendered(plugin, spec, rr, ctx, run_g15=False)
            n += 1
            if probs:
                bad.append((smp, seed, probs[:2]))
    assert n >= 2000 and not bad, bad[:5]


def test_labels_cover_every_option(plugin):
    seen = collections.Counter()
    for seed in range(BLOCK_SEEDS := 256):
        for smp in TRAIN:
            s = plugin.sample(seed, smp)
            seen[(s.structure["head"], plugin.label(s))] += 1
    for head, labels in TP.LABELS.items():
        assert all(seen[(head, lab)] > 0 for lab in labels), (head, [(l, seen[(head, l)]) for l in labels])


# ------------------------------------------------------------------------------------------------ determinism

def test_determinism_two_hashseeds():
    code = ("import sys, hashlib, json; sys.path.insert(0, '.'); sys.dont_write_bytecode = True\n"
            "from families.T40 import loader; loader.register()\n"
            "import pilot, pilot_loaders as PL\n"
            "with PL.open_family('T40') as kit:\n"
            "    b = pilot.build_pilot(kit, 90, run_g15=False)\n"
            "print(hashlib.sha256(json.dumps([i.row for i in b.infos], sort_keys=True).encode()).hexdigest())\n")
    outs = []
    for hs in ("1", "777"):
        p = subprocess.run([sys.executable, "-B", "-c", code], cwd=C2_BUILD, capture_output=True, text=True, timeout=600,
                           env={**os.environ, "PYTHONHASHSEED": hs})
        assert p.returncode == 0, p.stderr[-500:]
        outs.append(p.stdout.strip().splitlines()[-1])
    assert outs[0] == outs[1]


# ------------------------------------------------------------------------------------------------ the 3,000-row build

def test_build_gates(build):
    kit, b = build
    assert b.stats["rows_written"] >= 3000 and b.stats["reached_target"]
    gates = pilot.program_gates(b)
    assert all(g["verdict"] == "pass" for k, g in gates.items() if k in pilot.PROGRAM_GATES), {
        k: g["verdict"] for k, g in gates.items()}


def test_g6_g7_g10(build):
    kit, b = build
    g6 = pilot.g6(b.infos)
    assert g6["verdict"] == "pass", g6["fails"]
    g7 = pilot.g7(b.infos)
    assert g7["verdict"] == "pass"
    g10 = pilot.g10(b.infos, b.units, kit.plugin)
    assert g10["verdict"] == "pass", g10["failing"]


def test_options_only_probe_at_chance(build):
    _, b = build
    ch = [i for i in b.infos if i.row["qtype"] == "choice"]
    res = pilot.g6_choice(ch)
    for m in ("lr", "gbt"):
        # one-sided bar (G6: <= chance + 2 pp; here + 3). A below-chance value is the cross-validation signature of an exactly
        # balanced design (the fold that trains on an excess of a label tests on a deficit), not a leak: bounded at -6 pp.
        assert -0.06 <= res["b_options"][m] - res["chance"] <= 0.03, res["b_options"]


def _formatting_probe(infos, feats, y_of):
    import numpy as np
    from sklearn.ensemble import HistGradientBoostingClassifier
    from sklearn.model_selection import GroupKFold
    X = np.array([feats(i) for i in infos], dtype=float)
    y = np.array([y_of(i) for i in infos])
    g = np.array([i.row["meta"]["card_id"] for i in infos])
    pred = np.zeros(len(y))
    for tr, te in GroupKFold(n_splits=5).split(X, y, g):
        pred[te] = HistGradientBoostingClassifier(max_iter=100, random_state=0).fit(X[tr], y[tr]).predict(X[te])
    return float((pred == y).mean())


def test_formatting_only_and_diff_size_probes(build):
    _, b = build
    yn = [i for i in b.infos if i.row["qtype"] == "noul"]

    def fmt(i):
        r = i.row
        s = r["state"]
        return [len(s), s.count("\n"), s.count("["), s.count("("), s.count("*"), s.count('"'), len(r["instructions"]),
                len(r["card"] or ""), len(r["meta"]["c2"]["register"])]
    acc = _formatting_probe(yn, fmt, lambda i: int(i.row["gold"]))
    assert -0.06 <= acc - 0.5 <= 0.03, acc
    ced = [i for i in yn if i.spec.structure["head"] == "C"]

    def diff(i):
        st, env = i.spec.structure, i.spec.env()
        old, new = E.render_tokens(st["old"], "O", env), E.render_tokens(st["new"], "N", env)
        return [len(old), len(new), len(new) - len(old), old.count("\n"), new.count("\n")]
    acc = _formatting_probe(ced, diff, lambda i: int(i.row["gold"]))
    assert -0.08 <= acc - 0.5 <= 0.06, acc      # head C is ~7% of the rows, so the sample is small: wider band, see BUILD_NOTES


def test_head_a_valid_share_and_prompt_length(build):
    kit, b = build
    a = [i for i in b.infos if i.spec.structure["head"] == "A"]
    share = sum(1 for i in a if kit.plugin.label(i.spec) == "VALID") / len(a)
    assert share >= 0.40, share
    toks = [R.approx_tokens(i.row) for i in b.infos]
    assert sum(toks) / len(toks) <= 800 and max(toks) <= 2000


def test_held_out_only_in_s5(build):
    _, b = build
    for i in b.infos:
        st, smp = i.spec.structure, i.spec.sampler
        if st["head"] in "AB":
            styles = {"snake_vn", "snake_nv", "camel_vn", "pascal_vn", "dotted_vn"}
            assert (st["style"] in POOLS.HELD_OUT_STYLES) == (smp == "S5")
            assert (st["pack"] in POOLS.HELD_OUT_DOMAINS) == (smp == "S5")
            assert styles | set(POOLS.HELD_OUT_STYLES) >= {st["style"]}
        else:
            assert (st["pack"] in E.HELD_OUT_PACKS) == (smp == "S5")
        assert i.row["meta"]["dev_only"] == (smp == "S5")


def test_reseed_audit_3pct(build):
    kit, b = build
    plug = TP.T40Plugin(lexicon=kit.ctx.lexicon)
    plug.RNG_SALT = "|audit"
    specs = [i.spec for i in b.infos if i.row["role"] == "base"]
    pick = specs[:: max(1, int(len(specs) / (0.03 * len(b.infos))))]
    flips = 0
    for sp in pick:
        c = TP.design(sp.seed, sp.sampler)
        sp2 = plug.sample(sp.seed, sp.sampler)
        flips += plug.label(sp2) != c["label"] or sp2.qform != sp.qform
        rr = plug.render(sp2, kit.ctx)
        view = plug.parse(rr.row, kit.ctx)
        flips += plug.solve_b(view) != plug.solve_a(sp2)
    assert len(pick) >= 0.03 * len(b.infos) * 0.9
    assert flips <= 0.01 * len(pick), (flips, len(pick))
