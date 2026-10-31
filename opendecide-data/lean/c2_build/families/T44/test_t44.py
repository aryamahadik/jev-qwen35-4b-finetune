"""In-memory tests of the T44 plugin (nothing is written; no row file, no sealed split).

  contract      validate_plugin: only the yes/no complement requirement is open (choice-only family)
  A == B        T44_N_AB (default 2,000) sampled specs, 400 per sampler: render, parse (G3 facts == canonical), solver B
                == solver A == row gold, every option text reads back to its key; PLUS 3,000 random plans (garbage steps,
                negative goals) where forward simulation (A) must equal backward regression (B)
  bug caught    an injected solver-A bug is caught as a G2 mismatch
  algebras      >= 150 distinct random tool algebras in the training samplers
  held out      S5 vocabularies (domains, tools, predicates, types, objects, layouts) are disjoint from training and never
                appear in S1-S4 rows; training plans <= 6 steps / calls; S5 plans 7-8; only S5 rows are dev_only
  balance       head-1 labels exactly balanced per block of 4 seeds; the printed STEP k is the true k on STEP rows and
                independent of the label
  layouts       every register round-trips through parse
  tokens        mean <= 800, max <= 2,000 (instructions counted twice)
  determinism   the same rows under PYTHONHASHSEED 1 and 2
Run (from lean/c2_build):  ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T44/test_t44.py
"""
from __future__ import annotations

import collections
import hashlib
import os
import random
import re
import subprocess
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import plugin as KP  # noqa: E402
from c2_kit import rows as KR  # noqa: E402
from c2_kit.choiceplan import plan_report  # noqa: E402
from families.T44 import plugin as P  # noqa: E402
from families.T44 import solver_b as B  # noqa: E402
from families.T44 import texts as TX  # noqa: E402
from families.T44 import world as W  # noqa: E402

N_AB = int(os.environ.get("T44_N_AB", "2000"))
TRAIN = ("S1", "S2", "S3", "S4")


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
            except KP.ContractError as e:
                failed.append((smp, seed, str(e)[:60]))
    assert len(failed) <= 0.03 * per * len(P.SAMPLERS), failed[:5]
    return out


def test_contract(kit):
    plugin, ctx = kit
    probs = KP.validate_plugin(plugin, strict=True)
    rest = [p for p in probs if "complement" not in p]
    assert rest == [], rest
    assert ctx.lexicon.gate()["pass"]
    assert plugin.PARADIGM_A != plugin.PARADIGM_B
    assert KP.check_independence(plugin) == []
    assert len(Path(plugin.G0_LITE).read_text().splitlines()) <= 200


def test_solver_a_equals_b(kit, specs):
    plugin, ctx = kit
    assert len(specs) >= 0.97 * N_AB
    bad = []
    for sp in specs:
        rr = plugin.render(sp, ctx)
        view = plugin.parse(rr.row, ctx)
        a, b = plugin.solve_a(sp), plugin.solve_b(view)
        keys = view["options"]
        if not (a == b == rr.answer and keys[rr.row["options"].index(rr.row["gold"])] == b
                and {k: v for k, v in view.items() if k != "options"} == plugin.canonical(sp)):
            bad.append((sp.sampler, sp.seed, a, b))
    assert bad == [], bad[:5]


def _view(alg, objs, start, plan, goal):
    return {"qform": TX.HEAD_VERDICT, "tools": [[t["name"], t["params"], t["needs"], t["adds"], t["dels"]] for t in alg["tools"]],
            "objects": objs, "start": start, "goal": goal, "plan": plan}


def test_random_plans_forward_equals_regression():
    R = random.Random(20261015)
    seen = collections.Counter()
    for it in range(3000):
        dom = R.choice(W.TRAIN_DOMAINS + W.HELD_OUT_DOMAINS)
        alg = W.make_algebra(dom, R.randrange(W.ALGS_PER_DOMAIN))
        objs = W.make_objects(R, alg, dom)
        acts = W.ground_actions(alg, objs)
        s0 = W.make_start(R, alg, objs)
        start = [[p, list(a)] for p, a in sorted(s0)]
        walk = W.random_walk(R, acts, s0, R.randint(1, 6)) if R.random() < 0.65 else None
        if walk:
            plan = [[nm, list(a)] for nm, a in walk[0]]
        else:
            plan = [[g["call"][0], list(g["call"][1])] for g in (R.choice(acts) for _ in range(R.randint(1, 6)))]
        if R.random() < 0.12:                                     # garbage step
            j = R.randrange(len(plan))
            plan[j] = [R.choice(["zzz", plan[j][0]]), plan[j][1][:-1] if R.random() < 0.5 and plan[j][1] else plan[j][1] + ["nope"]]
        facts = W.all_facts(alg, objs)
        goal = W.make_goal(R, s0, walk[1][-1], R.randint(1, 3)) if walk and R.random() < 0.6 else None
        goal = goal or [[R.random() < 0.3, f[0], list(f[1])] for f in R.sample(facts, min(len(facts), R.randint(1, 3)))]
        a = W.verdict(alg, objs, start, plan, goal)
        b = B._verdict(_view(alg, objs, start, plan, goal))
        seen[a.split("_")[0]] += 1
        assert a == b, (it, dom, a, b, plan)
    assert all(seen[k] >= 100 for k in ("INVALID", "STEP", "GOAL", "VALID")), seen


def test_executor_semantics():
    alg = {"id": "t", "domain": "git", "tools": [W.parse_tool("a(x:t) :: needs not p(x) :: add p(x) :: del q(x)"),
                                                 W.parse_tool("b(x:t) :: needs p(x), q(x) :: add r(x)")]}
    objs = {"t": ["o1", "o2"]}
    start = [["q", ["o1"]]]
    goal = [[False, "r", ["o1"]]]
    assert W.verdict(alg, objs, start, [["a", ["o1"]], ["b", ["o1"]]], goal) == "STEP_2_NOT_APPLICABLE"   # a removed q
    assert W.verdict(alg, objs, start, [["a", ["o1"]], ["a", ["o1"]]], goal) == "STEP_2_NOT_APPLICABLE"   # not p fails
    assert W.verdict(alg, objs, start, [["a", ["o1"]]], goal) == "GOAL_NOT_REACHED"
    assert W.verdict(alg, objs, start, [["a", ["o9"]]], goal) == "INVALID"
    assert W.verdict(alg, objs, start, [["a", []]], goal) == "INVALID"
    assert W.verdict(alg, objs, start, [["c", ["o1"]]], goal) == "INVALID"
    acts = W.ground_actions({"tools": [W.parse_tool("a(x:t) :: add p(x)"), W.parse_tool("b(x:t) :: needs p(x) :: add r(x)"),
                                       W.parse_tool("c(x:t) :: add r(x)")]}, objs)
    ex = W.explore(acts, frozenset(), [[False, "r", ["o1"]]])
    assert ex["d"] == 1 and ex["firsts"] == {("c", ("o1",))}


def test_solver_b_catches_a_bug(kit, specs, monkeypatch):
    plugin, ctx = kit
    sp = next(s for s in specs if s.qform == TX.HEAD_VERDICT and plugin.solve_a(s) != TX.V_VALID)
    rr = plugin.render(sp, ctx)
    view = plugin.parse(rr.row, ctx)
    monkeypatch.setattr(W, "verdict", lambda *a, **k: TX.V_VALID)
    assert plugin.solve_a(sp) != plugin.solve_b(view)


def test_algebra_count(kit):
    plugin, _ = kit
    ids, structs = set(), set()
    for smp in TRAIN:
        for seed in range(500):
            dom, idx, alg = plugin._world(P.row_key(seed, smp, "x"), False)
            ids.add(alg["id"])
            structs.add(repr(alg["tools"]))
    assert len(ids) >= 150 and len(structs) >= 150, (len(ids), len(structs))
    assert len({i.split(":")[0] for i in ids}) == len(W.TRAIN_DOMAINS)


def test_held_out_vocabularies_disjoint():
    tv = [W.vocab(d) for d in W.TRAIN_DOMAINS]
    hv = [W.vocab(d) for d in W.HELD_OUT_DOMAINS]
    for k in ("tools", "preds", "types", "objects"):
        a, b = set().union(*[v[k] for v in tv]), set().union(*[v[k] for v in hv])
        assert a and b and not (a & b), (k, a & b)
    assert not set(TX.HELD_OUT_REGISTERS) & set(TX.TRAIN_REGISTERS)
    words = {w for r in TX.REGISTERS.values() for w in r["labels"]} | {"Tools", "Objects", "Start", "Goal", "Plan"}
    names = set().union(*[v[k] for v in tv + hv for k in v])
    assert not {w.rstrip(":") for w in words} & names                     # a layout label is never a name


def test_held_out_configuration(kit, specs):
    plugin, ctx = kit
    held_names = set().union(*[W.vocab(d)[k] for d in W.HELD_OUT_DOMAINS for k in ("tools", "preds", "types", "objects")])
    held_names |= set(TX.HELD_OUT_REGISTERS)
    for sp in specs:
        st = sp.structure
        rr = plugin.render(sp, ctx)
        toks = set(re.findall(r"[A-Za-z0-9_.\-]+", rr.row["state"]))
        if sp.sampler in TRAIN:
            assert st["domain"] in W.TRAIN_DOMAINS and st["n"] <= P.MAX_TRAIN_LEN
            assert not toks & held_names, (sp.sampler, sp.seed, toks & held_names)
            assert rr.skin_id.split("-")[-1] in TX.TRAIN_REGISTERS and not rr.row["meta"]["dev_only"]
        else:
            assert st["domain"] in W.HELD_OUT_DOMAINS and st["n"] in (7, 8)
            assert rr.skin_id.split("-")[-1] in TX.HELD_OUT_REGISTERS and rr.row["meta"]["dev_only"]
            if sp.qform == TX.HEAD_VERDICT:
                assert len(st["plan"]) in (7, 8)
            else:
                assert len(st["prefix"]) + st["d"] in (7, 8) and st["d"] <= 5
    assert {s.sampler for s in specs if s.qform == TX.HEAD_NEXT} == set(P.SAMPLERS) - {"S1", "S3"}


def test_label_balance_and_printed_k(kit):
    plugin, _ = kit
    cnt = collections.Counter()
    kbylab = collections.defaultdict(list)
    for smp in ("S1", "S3"):
        for seed in range(400):
            sp = plugin.sample(seed, smp)
            lab = plugin.solve_a(sp)
            base = lab.split("_")[0]
            cnt[base] += 1
            kbylab[base].append(sp.structure["kshow"])
            if base == "STEP":
                assert lab == TX.V_STEP.format(k=sp.structure["kshow"])
    assert max(cnt.values()) - min(cnt.values()) <= 2, cnt                 # exact per block of 4 seeds
    means = [sum(v) / len(v) for v in kbylab.values()]
    assert max(means) - min(means) < 0.35, means


def test_every_register_roundtrips(kit):
    plugin, ctx = kit
    for qf_sampler in ("S1", "S2"):
        sp = plugin.sample(11, qf_sampler)
        for reg in TX.REGISTERS:
            sk = ctx.skins[f"T44-SK-{reg}"]
            rr = plugin.render(sp, ctx, skin=sk)
            view = plugin.parse(rr.row, ctx)
            assert {k: v for k, v in view.items() if k != "options"} == plugin.canonical(sp), reg


def test_tokens_and_budget(kit, specs):
    plugin, ctx = kit
    rows = [plugin.render(s, ctx).row for s in specs if s.sampler in TRAIN][:600]
    est = [KR.approx_tokens(r) for r in rows]
    assert sum(est) / len(est) <= 800 and max(est) <= 2000
    assert all(not KR.validate_row(r, training=True) for r in rows)


def test_plan_report_and_option_names(kit, specs):
    """Position, abstain and gold-is-longest balance (kit plan_report) and the gold's rank in the kit's length order
    (length, then text: the order build_options plans), which is exactly uniform; every wrong option has a named model."""
    plugin, ctx = kit
    sets = [plugin.render(s, ctx).option_set for s in specs if s.sampler in TRAIN][:1200]
    rep = plan_report(sets)
    assert not [f for f in rep["failing"] if not f.startswith("length rank")], rep["failing"]
    ranks = collections.Counter()
    for s in sets:
        order = sorted(s.texts, key=lambda t: (len(t), t))
        ranks[order.index(s.options[s.gold_index].text)] += 1
    assert max(ranks.values()) - min(ranks.values()) <= 0.12 * len(sets) / 4 + 5, ranks
    for sp in specs[:200]:
        os_ = plugin.render(sp, ctx).option_set
        assert all(o.err for o in os_.options if o.role == "error"), sp.seed


def test_g4_relations_hold(kit, specs):
    plugin, ctx = kit
    n = 0
    for sp in [s for s in specs if s.sampler in TRAIN][:120]:
        rels = plugin.relations(sp)
        assert len(rels) >= 3
        for r in rels:
            want = plugin.solve_a(sp) if r.expect in (None, "same") else r.expect
            assert plugin.solve_a(r.spec) == want, r.note
            n += 1
    assert n >= 360


def _rows_hash(seed_env):
    code = ("import sys; sys.path.insert(0, %r)\n"
            "from families.T44 import plugin as P\nimport hashlib, json\n"
            "pl, ctx = P.make_plugin()\nh = hashlib.sha256()\n"
            "for smp in P.SAMPLERS:\n"
            "    for seed in range(12):\n"
            "        r = pl.render(pl.sample(seed, smp), ctx).row\n"
            "        h.update(json.dumps(r, sort_keys=True).encode())\nprint(h.hexdigest())\n") % str(C2_BUILD)
    out = subprocess.run([sys.executable, "-B", "-c", code], env={**os.environ, "PYTHONHASHSEED": seed_env},
                         capture_output=True, text=True, cwd=str(C2_BUILD))
    assert out.returncode == 0, out.stderr[-500:]
    return out.stdout.strip()


def test_determinism_two_hash_seeds():
    assert _rows_hash("1") == _rows_hash("2")
