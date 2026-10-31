"""In-memory tests of the T42 plugin (nothing is written; no row file, no sealed split).

  contract       validate_plugin: only the complement-form requirement (yes/no overlay) is open: T42 has choice rows only
  hermetic       the executor: CPython 3.12, PYTHONHASHSEED=0, a 5 s cap, sockets / writes / subprocesses refused, two
                 runs agree, a diverging program is capped
  A == B         T42_N_AB (default 2,000) sampled specs, 400 per sampler: render, parse, solver B == solver A == the row
                 gold, every option text reads back to its key; equivalence labels re-derived by B's grid enumeration
  gold           equivalence: DIFFERS carries a witness that really differs; SAME has 10K fuzz, a clean grid and >= 95% coverage
  held out       training samplers never use the closure / MRO buckets, swap_args or wrong_slice_bound, numbered / tabs
                 layouts; S5 does (and only S5 rows are dev only)
  mutants        every distractor is the real output of its named mutant (re-executed here), printed by the one printer
  pairs          f and g go through the same printer; diff-bin marginals are label-blind
  determinism    same rows under PYTHONHASHSEED 1 and 2
Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T42/test_plugin.py
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

from c2_kit import pipeline  # noqa: E402
from c2_kit import plugin as KP  # noqa: E402
from c2_kit.choiceplan import plan_report  # noqa: E402
from families.T42 import executor as E  # noqa: E402
from families.T42 import mutate as M  # noqa: E402
from families.T42 import plugin as P  # noqa: E402
from families.T42 import solver_b as B  # noqa: E402

N_AB = int(os.environ.get("T42_N_AB", "2000"))
TRAIN = ("S1", "S2", "S3", "S4")
SAMPLE_FAILURES: list = []


@pytest.fixture(scope="module")
def kit():
    return P.make_plugin()


@pytest.fixture(scope="module")
def specs(kit):
    plugin, _ = kit
    per = N_AB // len(P.SAMPLERS)
    out, failed = [], []
    for smp in P.SAMPLERS:
        for seed in range(per):
            try:
                out.append(plugin.sample(seed, smp))
            except KP.ContractError as e:                  # a seed whose structure search found nothing: counted, bounded
                failed.append((smp, seed, str(e)[:60]))
    assert len(failed) <= 0.02 * per * len(P.SAMPLERS), failed[:5]
    SAMPLE_FAILURES[:] = failed
    return out


# ------------------------------------------------------------------------------------------------ contract / executor
def test_contract(kit):
    plugin, ctx = kit
    probs = KP.validate_plugin(plugin, strict=True)
    rest = [p for p in probs if "complement" not in p]
    assert rest == [], rest
    assert KP.validate_plugin(plugin, strict=False) == [p for p in probs if "complement" not in p and "frozen" not in p]
    assert ctx.lexicon.gate()["pass"]


def test_hermetic_executor():
    r = E.run_snippets([
        {"id": "ok", "code": "print(sum(range(5)))", "kind": "print"},
        {"id": "hash", "code": "print(hash('abc'))", "kind": "print"},
        {"id": "sock", "code": "import socket\ns = socket.socket()", "kind": "print"},
        {"id": "write", "code": "open('x.txt', 'w').write('a')", "kind": "print"},
        {"id": "proc", "code": "import subprocess\nsubprocess.run(['ls'])", "kind": "print"},
        {"id": "loop", "code": "while True:\n    pass", "kind": "print"},
        {"id": "exc", "code": "d = {}\nprint(d['k'])", "kind": "print"},
    ], confirm=True)
    assert r["ok"]["out"] == "10\n"
    assert E.answer_key(r["sock"]) is None and E.answer_key(r["write"]) is None and E.answer_key(r["proc"]) is None
    assert r["loop"]["s"] == "cap" and E.answer_key(r["loop"]) is None
    assert E.answer_key(r["exc"]) == "exc:KeyError"
    h = E.run_one("print(hash('abc'))", "print")["out"]
    out = subprocess.run([E.python_exe(), "-S", "-c", "print(hash('abc'))"], env={"PYTHONHASHSEED": "0"},
                         capture_output=True, text=True).stdout
    assert h == out                                         # the child runs with PYTHONHASHSEED=0
    assert E.TIMEOUT_S == 5
    assert str(E.python_exe()).endswith(".venv/bin/python")


def test_equiv_rule_and_coverage():
    f = "def f(xs: list[int]):\n    t = 0\n    for x in xs:\n        if x > 3:\n            t += x\n    return t"
    same = "def g(xs: list[int]):\n    return sum(x for x in xs if x > 3)"
    typ = "def g(xs: list[int]):\n    return sum(x for x in xs if x >= 3)"
    edge = "def g(xs: list[int]):\n    return sum(x for x in xs if abs(x) > 3)"
    dead = "def g(xs: list[int]):\n    t = 0\n    for x in xs:\n        if x > 3:\n            t += x\n        elif x == 99999:\n            t += 0\n    return t"
    lab = lambda g: E.equiv_label(E.run_equiv(f, g, ("ints",), seed=3, confirm=True))  # noqa: E731
    assert lab(same) == ("SAME", None)
    assert lab(typ)[0] == "DIFFERS_TYPICAL"
    assert lab(edge)[0] == "DIFFERS_EDGE"
    assert lab(dead)[0] is None                              # an unreachable branch: coverage below 95%
    r = E.run_equiv(f, same, ("ints",), seed=3)
    assert r["fuzz_n"] == 10_000 and E.coverage_of(r) == 1.0


# ------------------------------------------------------------------------------------------------ A == B
def test_solver_a_equals_b(kit, specs):
    plugin, ctx = kit
    assert len(specs) >= 0.99 * N_AB and len(specs) >= min(N_AB, 1950)        # <= 1% of the seeds found no structure
    bad = []
    for sp in specs:
        rr = plugin.render(sp, ctx)
        view = plugin.parse(rr.row, ctx)
        a = plugin.solve_a(sp)
        b = plugin.solve_b(view)
        keys = view["options"]
        if not (a == b == rr.answer and keys[rr.row["options"].index(rr.row["gold"])] == b
                and {k: v for k, v in view.items() if k != "options"} == plugin.canonical(sp)):
            bad.append((sp.sampler, sp.seed, a, b))
    assert bad == [], bad[:5]


def test_solver_independence(kit):
    plugin, _ = kit
    assert KP.check_independence(plugin) == []
    assert plugin.PARADIGM_A != plugin.PARADIGM_B


def test_solver_b_catches_a_bug(kit, specs, monkeypatch):
    plugin, ctx = kit
    sp = next(s for s in specs if s.qform == "ch_output" and s.sampler == "S1")
    rr = plugin.render(sp, ctx)
    monkeypatch.setattr(B, "key_of", lambda *a, **k: "out:bogus")
    probs = pipeline.check_rendered(plugin, sp, rr, ctx, run_g15=False)
    assert any(g == "G2" for g, _ in probs)


# ------------------------------------------------------------------------------------------------ gold
def test_equivalence_gold(kit, specs):
    plugin, _ = kit
    eq = [s for s in specs if s.qform == "ch_equiv"]
    assert len(eq) >= 0.15 * N_AB
    for s in eq[:120]:
        st = s.structure
        res = E.run_equiv(st["f"], st["g"], tuple(st["sig"]), seed=P._fuzz_seed(st["f"], st["g"]), confirm=True)
        label, w = E.equiv_label(res)
        assert label == st["label"] == plugin.solve_a(s)
        if label == "SAME":
            assert res["fuzz_n"] == 10_000 and res["cross_diff"] == 0 and res["fuzz_diff"] == 0
            assert E.coverage_of(res) >= 0.95
        else:
            assert w is not None                                      # a witness by execution
            ns_f, ns_g = {}, {}
            exec(st["f"], ns_f)
            exec(st["g"], ns_g)
            args = [list(x) if isinstance(x, list) else x for x in w]
            args2 = [list(x) if isinstance(x, list) else x for x in w]

            def run(fn, a):
                try:
                    return ("v", repr(fn(*a)), repr(a))
                except Exception as e:  # noqa: BLE001
                    return ("e", type(e).__name__)
            assert run(ns_f["f"], args) != run(ns_g["g"], args2)
    labs = collections.Counter(s.structure["label"] for s in eq)
    assert min(labs.values()) / len(eq) > 1 / 3 - 4 * (2 / 9 / len(eq)) ** 0.5, labs      # label thirds


def test_pairs_use_one_printer(specs):
    import ast
    for s in specs:
        if s.qform == "ch_equiv":
            f, g = s.structure["f"], s.structure["g"]
            assert f == ast.unparse(ast.parse(f)) and g == ast.unparse(ast.parse(g))
        else:
            c = s.structure["code"]
            assert c == ast.unparse(ast.parse(c))
            for d in s.structure["distractors"]:
                assert d["code"] == ast.unparse(ast.parse(d["code"]))


def test_diff_bin_is_label_blind(specs):
    eq = [s for s in specs if s.qform == "ch_equiv" and s.sampler in TRAIN]
    bins = collections.defaultdict(collections.Counter)
    for s in eq:
        bins[s.structure["label"]][s.structure["diff_bin"]] += 1
    shares = {lab: [c[b] / sum(c.values()) for b in range(4)] for lab, c in bins.items()}
    for b in range(4):
        vals = [shares[lab][b] for lab in shares]
        nmin = min(sum(c.values()) for c in bins.values())
        assert max(vals) - min(vals) < 0.03 + 4 * (0.25 / nmin) ** 0.5, (b, shares)


# ------------------------------------------------------------------------------------------------ mutants
def test_every_distractor_is_a_real_mutant_output(kit, specs):
    out = [s for s in specs if s.qform != "ch_equiv"][:150]
    jobs = []
    for i, s in enumerate(out):
        for j, d in enumerate(s.structure["distractors"]):
            jobs.append({"id": f"{i}.{j}", "code": d["code"], "kind": s.structure["kind"]})
    res = E.run_snippets(jobs, confirm=True)
    for i, s in enumerate(out):
        for j, d in enumerate(s.structure["distractors"]):
            assert E.answer_key(res[f"{i}.{j}"]) == d["key"] != plugin_gold(s)
            assert d["ops"] and all(o in M.OPERATORS or o == "compound" for o in d["ops"])
            assert d["code"] != s.structure["code"]


def plugin_gold(s):
    return E.answer_key(E.run_one(s.structure["code"], s.structure["kind"]))


def test_option_sets_are_planned(kit, specs):
    plugin, ctx = kit
    sets = [plugin.render(s, ctx).option_set for s in specs if s.sampler in TRAIN and s.qform != "ch_equiv"]
    rep = plan_report(sets)
    n = len(sets)
    bar = 2.0 if n >= 1500 else 2.0 + 250 / n ** 0.5            # the +/- 2 pp bar is for pilot-size n
    assert rep["longest_gold_pp"] is None or abs(rep["longest_gold_pp"]) <= bar + 1e-9, rep
    assert {len(s.options) for s in sets} <= {4, 5}


def test_exceptions_balanced_within_the_exception_idiom(specs):
    rows = [s for s in specs if s.qform != "ch_equiv" and s.sampler in TRAIN]
    exc_idiom = [s for s in rows if s.structure["template"] == "exc_fail"]
    other = [s for s in rows if s.structure["template"] != "exc_fail"]
    assert exc_idiom and all(d["key"].startswith("out:") for s in other for d in s.structure["distractors"])
    assert all(s.structure["gold_kind"] == "out" for s in other)


# ------------------------------------------------------------------------------------------------ held out
def test_held_out_configuration(kit, specs):
    plugin, ctx = kit
    train_out = [s for s in specs if s.sampler in TRAIN and s.qform != "ch_equiv"]
    s5_out = [s for s in specs if s.sampler == "S5" and s.qform != "ch_equiv"]
    assert train_out and s5_out
    assert all(s.structure["idiom"] not in ("closure", "mro") for s in train_out)
    assert all(s.structure["idiom"] in ("closure", "mro") for s in s5_out)
    used = {o for s in train_out for d in s.structure["distractors"] for o in d["ops"]}
    assert not used & set(M.HELD_OUT_OPS) and not used & set(M.BUCKET_OPS)
    for s in specs:
        if s.qform == "ch_equiv" and s.sampler in TRAIN:
            assert s.structure["mut_op"] not in M.HELD_OUT_OPS
    s5_used = {o for s in s5_out for d in s.structure["distractors"] for o in d["ops"]}
    assert s5_used & set(M.HELD_OUT_OPS)
    for smp in ("S1", "S5"):
        sp = next(s for s in specs if s.sampler == smp)
        rr = plugin.render(sp, ctx)
        assert rr.row["meta"]["dev_only"] is (smp == "S5")
        assert (rr.row["meta"]["c2"]["register"] in P.HELD_OUT_REGISTERS) is (smp == "S5")


def test_tokens_and_balance(kit, specs):
    plugin, ctx = kit
    rows = [plugin.render(s, ctx).row for s in specs[:300]]
    from c2_kit import rows as R
    toks = [R.approx_tokens(r) for r in rows]
    assert max(toks) <= 2000 and sum(toks) / len(toks) <= 800
    assert all(not R.validate_row(r) for r in rows)


# ------------------------------------------------------------------------------------------------ determinism
SCRIPT = """
import sys, json, hashlib
sys.path.insert(0, %r)
from families.T42 import plugin as P
plugin, ctx = P.make_plugin()
rows = []
for smp in ("S1", "S3", "S4", "S5"):
    for seed in range(6):
        rows.append(plugin.render(plugin.sample(seed, smp), ctx).row)
print(hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest())
"""


def test_determinism_across_hashseeds():
    outs = []
    for seed in ("1", "2"):
        env = {**os.environ, "PYTHONHASHSEED": seed}
        p = subprocess.run([sys.executable, "-B", "-c", SCRIPT % str(C2_BUILD)], env=env, capture_output=True, text=True,
                           cwd=str(C2_BUILD))
        assert p.returncode == 0, p.stderr[-500:]
        outs.append(p.stdout.strip().splitlines()[-1])
    assert outs[0] == outs[1] and len(outs[0]) == 64
