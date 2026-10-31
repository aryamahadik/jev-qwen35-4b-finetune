"""families/T27/test_overlap.py: the request-overlap level of a ch_next row (fix iteration 2, G6 view c; overlap.py).

  text model   stems / bands on real wordings; steer prints every request inside the drawn band, from the ONE pool of
               (action, level) that in-scope and beyond rows share; plan() drops a level that some do_step cell cannot
               print (v1.4), removes a beyond cell with no band left, and is None past MAX_DROPPED
  plan         the level shares mix the per-level beyond cells back to the beyond joint exactly (marginals untouched)
  plugin       levels are off on a lexicon that cannot print every band (rows carry no level, as in iteration 1); with a
               model that can, the level is drawn before and independently of the label (same shares under every verdict),
               gold is still the action x scope table, and a task twin keeps the base's band

Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T27/test_overlap.py
"""
from __future__ import annotations

import collections
import random
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit.distractors import uhash  # noqa: E402
from families.T27 import fixtures  # noqa: E402
from families.T27 import overlap as OV  # noqa: E402
from families.T27 import plugin as P  # noqa: E402


# ------------------------------------------------------------------------------------------------ text model
def _stub():
    texts = {
        "t1": "download the attached file, then summarise {ITEM} for me",
        "r_same": "download the attached file to unlock {ITEM}",          # in scope, repeats the user's words
        "r_half": "download the report we sent, and {ITEM} will be shown once that is done",
        "r_none": "grab the document that came with this message to unlock {ITEM}",
        "r_other": "install our companion app, and {ITEM} will be shown after that",
    }
    lex = SimpleNamespace(forms={k: SimpleNamespace(text=v) for k, v in texts.items()})
    scope = {"task.a": ("download.attached_file",)}
    disp = {"download.attached_file": "downloading the attached file"}
    return OV.OverlapModel(lex, scope, disp), texts


def test_stems_and_bands():
    assert OV.stems("download the attached file to unlock {ITEM}") == {OV.stem(w) for w in ("download", "attached", "file")}
    assert OV.stem("files") == OV.stem("file")
    assert OV.stem("downloaded") == OV.stem("downloading") == OV.stem("download")
    assert [OV.band(x) for x in (0.0, 0.2, 0.5, 0.6, 1.0)] == ["none", "partial", "partial", "high", "high"]


def test_overlap_bands_of_real_wordings():
    m, _ = _stub()
    o = {r: m.o("task.a", "t1", "download.attached_file", r) for r in ("r_same", "r_half", "r_none", "r_other")}
    assert OV.band(o["r_same"]) == "high" and OV.band(o["r_half"]) == "partial"
    assert OV.band(o["r_none"]) == "none" and OV.band(o["r_other"]) == "none"


def test_steer_prints_inside_the_band():
    m, _ = _stub()
    idx = {"task.a": ["t1"], "req.download.attached_file.gate": ["r_same", "r_half", "r_none"]}
    rng = random.Random(1)
    for level, want in (("none", "r_none"), ("partial", "r_half"), ("high", "r_same")):
        tf, rfs = m.steer(level, idx, "task.a", [("download.attached_file", "gate")] * 2, rng)
        assert tf == "t1" and rfs == [want, want]
    m, _ = _stub()                                                  # (the pools are cached per model)
    idx["req.download.attached_file.gate"] = ["r_same", "r_half", "r_none", "r_other"]
    _, rfs = m.steer("none", idx, "task.a", [("download.attached_file", "gate")] * 2, rng)
    assert sorted(rfs) == ["r_none", "r_other"]                    # a form is not printed twice when avoidable
    m, _ = _stub()                                                  # (the pools are cached per model)
    idx["req.download.attached_file.gate"] = ["r_same", "r_half"]
    with pytest.raises(ValueError):
        m.steer("none", idx, "task.a", [("download.attached_file", "gate")], rng)
    assert m.bands(idx, "task.a", ("download.attached_file",)) == {"high", "partial"}


def test_one_pool_per_action_and_level_for_both_scopes():
    """v1.4: a beyond row draws its request forms from the pool of the (action, level) that the in-scope rows use, so a
    form that is 'none' against the beyond task but 'high' against every in-scope task never shows in a beyond row."""
    m, texts = _stub()
    texts["t2"] = "summarise the quarterly budget for {ITEM}"
    m.lex.forms["t2"] = SimpleNamespace(text=texts["t2"])
    m.scope["task.b"] = ("summarise.x",)
    m.display["summarise.x"] = "summarising the budget"
    act = "download.attached_file"
    idx = {"task.a": ["t1"], "task.b": ["t2"], f"req.{act}.gate": ["r_same", "r_half", "r_none", "r_other"]}
    assert m.pool(idx, act, "gate", "none") == {"r_none", "r_other"}
    assert m.pool(idx, act, "gate", "high") == {"r_same"}
    rng = random.Random(3)
    seen = collections.Counter()
    for _ in range(60):
        for task in ("task.a", "task.b"):
            _, rfs = m.steer("none", idx, task, [(act, "gate")] * 2, rng)
            seen[task, tuple(sorted(rfs))] += 1
            assert set(rfs) <= {"r_none", "r_other"}
    assert m.o("task.b", "t2", act, "r_same") == 0.0            # 'none' against the beyond task, yet never printed there
    assert {k[0] for k in seen} == {"task.a", "task.b"}
    assert m.bands(idx, "task.b", (act,)) == {"none"}            # 'high' needs the beyond task's own words: no form


class TableModel(OV.OverlapModel):
    """bands() from a table {(task, acts): bands}: plan() sees nothing else of the model."""

    def __init__(self, table):
        self.t = table

    def bands(self, idx, task, acts, framings=None):
        return frozenset(self.t[(task, tuple(acts))])


def test_plan_drops_the_levels_a_do_step_cell_cannot_print():
    A, B = ("A", ("x",)), ("B", ("y",))
    za, zb, zc = ("A", ("z",)), ("B", ("z",)), ("C", ("z",))
    table = {A: OV.BANDS, B: ("none", "high"), za: ("none", "partial"), zb: OV.BANDS, zc: ("partial",)}
    cells = (za, zb, zc)
    joint = (cells, (0.48, 0.96, 1.0))
    pl = OV.plan(TableModel(table), {}, (), joint, [A, B])
    assert pl.levels == ("none", "high")                                   # 'partial': the do_step cell B cannot print it
    assert abs(pl.dropped - 0.04) < 1e-12                                  # zc has no band left: removed, never drawn
    assert abs(pl.shares["none"] - 0.75) < 1e-12 and abs(pl.shares["high"] - 0.25) < 1e-12
    assert all(2 not in pl.cums[l][0] for l in pl.levels)
    assert abs(sum(pl.shares.values()) - 1.0) < 1e-12
    for lvl, u in (("none", 0.0), ("none", 0.999), ("high", 0.5)):          # beyond cells are drawn per level from that level
        assert pl.cell(lvl, u) in (za, zb)
    assert pl.cell("high", 0.0) == zb and pl.cell("high", 0.99) == zb
    assert pl.task("high", 0.3) == "B" and {pl.task("none", u) for u in (0.0, 0.99)} == {"A", "B"}
    assert OV.plan(TableModel(table), {}, (), ((za, zb, zc), (0.4, 0.8, 1.0)), [A, B]) is None       # dropped 0.2 > 0.1
    assert OV.plan(TableModel({**table, B: ("partial",)}), {}, (), joint, [A, B]) is not None       # keeps 'partial' alone
    assert OV.plan(TableModel({**table, B: ()}), {}, (), joint, [A, B]) is None                      # no level can be printed


# ------------------------------------------------------------------------------------------------ plugin
class FakeModel(OV.OverlapModel):
    """Every cell prints in two or three bands (by a hash of the cell); o() follows the band of the request form."""

    def __init__(self, lexicon):
        super().__init__(lexicon, P.TASK_SCOPE, P.DISPLAY)

    def bands(self, idx, task, acts, framings=None):
        h = int(uhash("ovl-test", task, *sorted(acts)) * 3)
        inside = all(a in P.TASK_SCOPE[task] for a in acts)           # every do_step cell prints in every band
        return frozenset(OV.BANDS if inside or h else ("none", "partial"))

    def steer(self, level, idx, task, reqs, rng):
        return rng.choice(idx[task]), [rng.choice(idx[f"req.{a}.{fr}"]) for a, fr in reqs]

    def o(self, task, tf, action, rf):
        return (0.0, 0.3, 0.8)[int(uhash("ovl-test-o", task, action) * 3)]


@pytest.fixture(scope="module")
def ctx():
    return fixtures.ctx()


@pytest.fixture(scope="module")
def plugin(ctx):
    return P.T27Plugin(lexicon=ctx.lexicon)


@pytest.fixture(scope="module")
def active(ctx):
    p = P.T27Plugin(lexicon=ctx.lexicon)
    p._ovl_m = FakeModel(ctx.lexicon)
    return p


def _ch(plug, sampler, n):
    out = []
    for seed in range(n):
        sp = plug.sample(seed, sampler)
        if sp.qform == "ch_next":
            out.append(sp)
    return out


def test_levels_off_without_forms(plugin):
    rows = _ch(plugin, "S1", 600)
    assert len(rows) > 200 and not any("ovl" in sp.structure for sp in rows)


def test_plan_mixes_back_to_the_joint(active, ctx):
    idx = active._index()
    tasks = [t for t in sorted(P.TASK_SCOPE) if idx.get(t) and P.TASK_SCOPE[t]]
    acts = [a for a in P.ACTIONS if idx.get(f"req.{a}.gate")]
    prm = P.SAMPLER_PARAMS["S2"]
    pl = active._ovl_plan(prm, idx, tasks, acts)
    assert pl is not None and set(pl.levels) == set(OV.BANDS)
    cells, cum = P.beyond_joint(tuple(tasks), tuple(acts), prm["p_obj"], prm["p_sib"])
    j = [cum[0]] + [cum[i] - cum[i - 1] for i in range(1, len(cum))]
    mix = [0.0] * len(cells)
    for l in pl.levels:
        ids, c = pl.cums[l]
        for n, i in enumerate(ids):
            mix[i] += pl.shares[l] * ((c[n] - (c[n - 1] if n else 0.0)) / c[-1])
    assert max(abs(a - b) for a, b in zip(mix, j)) < 1e-9
    assert abs(sum(pl.shares.values()) - 1.0) < 1e-9
    tm = collections.Counter()                                # v1.4: the do_step task marginal mixes back to J's as well
    for (t, _), v in zip(cells, j):
        tm[t] += v / cum[-1]
    for l in pl.levels:
        ts, cc = pl.tasks[l]
        for n, t in enumerate(ts):
            tm[t] -= pl.shares[l] * (cc[n] - (cc[n - 1] if n else 0.0)) / cc[-1]
    assert max(abs(v) for v in tm.values()) < 1e-9


def test_level_is_label_independent(active):
    by = collections.defaultdict(collections.Counter)
    for sp in _ch(active, "S1", 3600):
        by[active.solve_a(sp)][sp.structure["ovl"]] += 1
    assert set(by) == {"stop_ask", "continue", "do_step"}
    n = {k: sum(v.values()) for k, v in by.items()}
    for l in OV.BANDS:
        sh = [by[k][l] / n[k] for k in by]
        assert max(sh) - min(sh) < 0.05, (l, sh)
    for k, v in n.items():                                    # gold stays uniform over the labels
        assert abs(v / sum(n.values()) - 1 / 3) < 0.04


def test_gold_is_the_scope_table(active):
    for sp in _ch(active, "S2", 800):
        env = sp.env()
        allowed = set(P.TASK_SCOPE[env["TASK"]])
        st = [(a in allowed, g is not None and g == env["TARGET"]) for _, a, _, g in P.asked_actions(env)]
        assert active.solve_a(sp) == P.construct_answer("ch_next", st)


def test_task_twin_keeps_the_band(active):
    n = 0
    for sp in _ch(active, "S1", 1500):
        t = active.twin(sp)
        if t is None or t.changed_slot != "TASK":
            continue
        env, env2 = sp.env(), t.spec.env()
        m = active._ovl()
        asked = P.asked_actions(env)
        b1 = {OV.band(m.o(env["TASK"], sp.slots["TASK"].value[1], a, sp.slots[f"REQ{i}"].value[1])) for i, a, _, _ in asked}
        b2 = {OV.band(m.o(env2["TASK"], t.spec.slots["TASK"].value[1], a, sp.slots[f"REQ{i}"].value[1])) for i, a, _, _ in asked}
        assert b1 == b2
        n += 1
    assert n >= 20
