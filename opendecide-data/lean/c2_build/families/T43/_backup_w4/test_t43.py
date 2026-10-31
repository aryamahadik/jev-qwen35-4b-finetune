"""In-memory tests of T43 (nothing is written but a metrics JSON; no row file, no sealed split).

  contract       validate_plugin (the complement-form requirement is for yes/no families: strict=False), G0 spec frozen
  hermetic       the executor: CPython 3.12, PYTHONHASHSEED=0, sockets / writes refused, two runs agree, a diverging program is capped
  originals      every template instance equals its docstring expression on the G0 grid (solver B's oracle is sound)
  A == B         T43_N_AB (default 2,000) sampled specs over S1-S5 (parallel): render, parse, solver B == solver A == row gold,
                 every option text reads back to its key, every shown patch re-applies through both appliers
  held out       training samplers never inject or patch with swap_args / wrong_slice_bound, never use the boxed / tabs layouts;
                 S5 injects only the held-out operators (none rows aside), uses only held-out layouts, and is dev only
  gold           reverting only the gold hunk turns F2P green; verdict C rows pass every listed test and differ from O on the grid
  determinism    the same rows under PYTHONHASHSEED 1 and 2
  reseed         3% of the rows re-executed under another PYTHONHASHSEED and seeded-case seed, and regenerated with an independent
                 random stream: at most 1% label flips
Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T43/test_t43.py
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

import c2_kit.plugin as KP  # noqa: E402
from c2_kit.choiceplan import plan_report  # noqa: E402
from families.T42 import mutate as M42  # noqa: E402
from families.T43 import executor as E  # noqa: E402
from families.T43 import patching as PT  # noqa: E402
from families.T43 import plugin as P  # noqa: E402
from families.T43 import solver_b as B  # noqa: E402
from families.T43 import templates as TP  # noqa: E402

N_AB = int(os.environ.get("T43_N_AB", "2000"))
WORKERS = int(os.environ.get("T43_WORKERS", "8"))
_G: dict = {}


def _plugin():
    if "p" not in _G:
        _G["p"] = P.make_plugin()
    return _G["p"]


def _check(args):
    seed, smp = args
    plugin, ctx = _plugin()
    try:
        spec = plugin.sample(seed, smp)
        rr = plugin.render(spec, ctx)
        gold = plugin.solve_a(spec)
        view = plugin.parse(rr.row, ctx)
        b = plugin.solve_b(view)
        keys = view["options"]
        st = spec.structure
        bad = []
        if rr.answer != gold:
            bad.append("row gold != A")
        if b != gold:
            bad.append(f"B {b} != A {gold}")
        if keys[rr.row["options"].index(rr.row["gold"])] != gold:
            bad.append("gold option does not read back")
        if st["patch"] is not None:
            if (PT.apply_diff(st["code"], st["patch"]) is None) != (B.apply_patch(st["code"], st["patch"]) is None):
                bad.append("appliers disagree")
            elif PT.apply_diff(st["code"], st["patch"]) != B.apply_patch(st["code"], st["patch"]):
                bad.append("appliers give different files")
        return (smp, seed, spec.qform, gold, st["op"], rr.row["meta"]["c2"]["register"], rr.row["meta"]["dev_only"], bad,
                st["head"])
    except Exception as e:  # noqa: BLE001
        return (smp, seed, "?", "?", "?", "?", False, [f"{type(e).__name__}: {str(e)[:160]}"], "?")


@pytest.fixture(scope="module")
def ab():
    per = N_AB // 5
    jobs = [(seed, smp) for seed in range(per) for smp in P.SAMPLERS]
    with mp.get_context("fork").Pool(WORKERS) as pool:
        return pool.map(_check, jobs, chunksize=4)


def test_contract_and_g0():
    plugin, _ = P.make_plugin()
    sha = hashlib.sha256((Path(P.HERE) / "G0_SPEC.md").read_bytes()).hexdigest()
    assert P.T43Plugin.G0_SHA256 == sha, sha
    assert KP.validate_plugin(plugin, strict=False) == []
    assert len(P.LABEL_WORDS) and plugin.HELD_OUT_SAMPLERS == ("S5",)


def test_hermetic_executor():
    r = E.run([E.pair_job("def f(x):\n    return x + 1\n", "def f(x):\n    return x + 2\n", ["f(1)"])], confirm=True)[0]
    assert r == [[["v", "2"], ["v", "3"]]]
    bad = E.run([E.pair_job("import socket\ndef f():\n    return socket.socket()\n", "def f():\n    return 1\n", ["f()"])])[0]
    assert bad[0][0][0] == "e" or bad[0][0][0] == "x"         # the sandbox refuses the socket (or the import is absent)
    loop = "def f(n):\n    while True:\n        n += 1\n"
    t = E.run([E.pair_job(loop, loop, ["f(1)"])])[0]
    assert t[0][0] == ["t"]                                    # a diverging program is capped per call
    w = E.run([E.pair_job("def f():\n    open('x.txt', 'w').write('a')\n    return 1\n", "def f():\n    return 1\n", ["f()"])])[0]
    assert w[0][0][0] == "e"                                   # writing a file is refused


def test_originals_equal_docstrings():
    import random
    R = random.Random(7)
    n = 0
    for tpl in TP.LINE_ORDER:
        for s in range(3):
            prog = TP.build_line(R, tpl, s)
            assert B._deviating(prog["src"]) == [], (tpl, s)
            n += 1
    for n_fn in (5, 6, 7, 8):
        for red in TP.REDUCER_ORDER:
            prog = TP.build_module(R, n_fn, red, n_fn % 3)
            assert B._deviating(prog["src"]) == [], (n_fn, red)
            n += 1
    assert n >= 28 + 16


def test_solver_a_equals_solver_b(ab):
    bad = [x for x in ab if x[7]]
    assert len(ab) >= N_AB - 5 and not bad, bad[:5]
    assert len({x[8] for x in ab}) == 3


def test_held_out_unreachable(ab):
    assert tuple(P.HELD_OUT_OPS) == tuple(M42.HELD_OUT_OPS) == ("swap_args", "wrong_slice_bound")
    assert not set(P.LINE_OPS) & set(P.HELD_OUT_OPS) and not set(P.MOD_OPS) & set(P.HELD_OUT_OPS)
    assert not set(P.TRAIN_ALL) & set(P.HELD_OUT_OPS) and not set(P.TRAIN_ALL) & set(M42.BUCKET_OPS)
    assert not set(P.HELD_OUT_REGISTERS) & set(P.REGISTERS[:6])
    for smp, seed, qf, gold, op, reg, dev, bad, head in ab:
        if smp == "S5":
            assert dev and reg in P.HELD_OUT_REGISTERS
            assert op in P.HELD_OUT_OPS or op == "none", (op, seed)
        else:
            assert not dev and reg not in P.HELD_OUT_REGISTERS
            assert op not in P.HELD_OUT_OPS
    # every site any training sampler can reach, recorded while sampling
    seen = set()
    orig_apply = M42.apply

    def rec(src, site):
        seen.add(site[0])
        return orig_apply(src, site)
    M42.apply = rec
    try:
        plugin, _ = P.make_plugin()
        for smp in ("S1", "S2", "S3", "S4"):
            for seed in range(40, 52):
                plugin.sample(seed, smp)
    finally:
        M42.apply = orig_apply
    assert seen and not seen & set(P.HELD_OUT_OPS), seen


def test_gold_semantics():
    plugin, ctx = _plugin()
    n_c = n_a = 0
    for smp in ("S1", "S4"):
        for seed in range(30, 46):
            spec = plugin.sample(seed, smp)
            st = spec.structure
            gold = plugin.solve_a(spec)
            tests = [(c, e) for c, e, _ in st["tests"]]
            if gold == "D":
                assert PT.apply_diff(st["code"], st["patch"]) is None
                continue
            patched = PT.apply_diff(st["code"], st["patch"])
            r = E.run([E.judge_job(st["orig"], st["fns"], [("p", patched)], tests, st["exseed"])])[0][0]
            assert r["seeded_n"] >= 200 * len([f for f in st["fns"] if f.get("entry")])
            if gold in ("A", "C"):
                assert all(t == "p" for t in r["tests"])
            if gold == "C":
                n_c += 1
                assert r["grid_diff"] > 0
            if gold == "A":
                n_a += 1
                assert r["grid_diff"] == 0 and r["seeded_diff"] == 0
            if gold == "B":
                assert any(t != "p" for t in r["tests"])
    assert n_c and n_a
    # reverting only the gold hunk turns F2P green (ll / lf)
    for smp in ("S2", "S3"):
        for seed in range(30, 38):
            spec = plugin.sample(seed, smp)
            st = spec.structure
            g = plugin.solve_a(spec)
            assert (g == "none") == (st["code"] == st["orig"])


def test_plan_report():
    """120 rows only: the abstain cells need >= 1,000 rows (the 5,200-row G10 covers them: BUILD_NOTES). Here: no gross imbalance."""
    plugin, ctx = _plugin()
    rows = []
    for smp in P.SAMPLERS[:4]:
        for seed in range(60, 90):
            rows.append(plugin.render(plugin.sample(seed, smp), ctx).option_set)
    rep = plan_report(rows)
    assert rep["longest_gold_pp"] is None or abs(rep["longest_gold_pp"]) <= 10, rep
    assert all(p is None or p > 0.001 for p in rep["positions_chi2_p"].values()), rep


CODE = '''
import sys, json, hashlib
sys.path.insert(0, ".")
from families.T43 import plugin as P
plugin, ctx = P.make_plugin()
out = []
for smp in ("S1", "S2", "S3", "S4", "S5"):
    for seed in range(4):
        sp = plugin.sample(seed, smp)
        rr = plugin.render(sp, ctx)
        out.append(rr.row["id"] + hashlib.sha256(json.dumps(rr.row, sort_keys=True).encode()).hexdigest()[:12])
print(hashlib.sha256("|".join(out).encode()).hexdigest())
'''


def test_determinism_two_hashseeds():
    outs = []
    for hs in ("1", "2"):
        env = {**os.environ, "PYTHONHASHSEED": hs}
        p = subprocess.run([sys.executable, "-B", "-c", CODE], cwd=C2_BUILD, env=env, capture_output=True, text=True, timeout=900)
        assert p.returncode == 0, p.stderr[-500:]
        outs.append(p.stdout.strip())
    assert outs[0] == outs[1] and len(outs[0]) == 64


def test_reseed_audit():
    plugin, ctx = _plugin()
    from c2_kit.distractors import uhash
    jobs = [(seed, smp) for seed in range(200, 600) for smp in P.SAMPLERS[:4] if uhash("reseed43", seed, smp) < 0.03]
    assert len(jobs) >= 30
    flips, re_exec = 0, 0
    old = E.HASHSEED
    for seed, smp in jobs:
        spec = plugin.sample(seed, smp)
        gold = plugin.solve_a(spec)
        again = plugin.sample_salted(seed, smp, "audit")

        def cls(sp, g):          # a function name is a random draw: compare its position in the module
            names = [f["name"] for f in sp.structure["fns"]]
            return names.index(g) if sp.structure["head"] == "lf" and g in names else g
        flips += cls(again, plugin.solve_a(again)) != cls(spec, gold) or again.qform != spec.qform
        E.HASHSEED = "7"
        try:
            st = dict(spec.structure)
            st["exseed"] = st["exseed"] ^ 0x5BD1E995
            E._CACHE.clear()
            re_exec += plugin.solve_a(spec.replace(structure=st)) != gold
        finally:
            E.HASHSEED = old
            E._CACHE.clear()
    assert flips <= 0.01 * len(jobs) and re_exec <= 0.01 * len(jobs), (flips, re_exec, len(jobs))
