"""pytest for T45 TRACE-VERIFY (from lean/c2_build):  ../../.venv/bin/python -m pytest -q -p no:cacheprovider families/T45/test_t45.py
Env: T45_N_AB (default 2000 specs for A == B), T45_BUILD_N (default 300 rows through pilot.build_pilot; 3000 for the full gate run)."""
from __future__ import annotations

import json
import os
import random
import re
import subprocess
import sys
from pathlib import Path

import pytest

C2 = Path(__file__).resolve().parents[2]
if str(C2) not in sys.path:
    sys.path.insert(0, str(C2))

from c2_kit import plugin as KP  # noqa: E402
from c2_kit import pipeline  # noqa: E402
from c2_kit.choiceplan import plan_report  # noqa: E402
from c2_kit.rows import approx_tokens  # noqa: E402
from families.T45 import audits as AU  # noqa: E402
from families.T45 import executor as E  # noqa: E402
from families.T45 import plugin as P  # noqa: E402
from families.T45 import scenarios as SC  # noqa: E402
from families.T45 import solver_b as B  # noqa: E402
from families.T45 import texts as TX  # noqa: E402

N_AB = int(os.environ.get("T45_N_AB", "2000"))
BUILD_N = int(os.environ.get("T45_BUILD_N", "300"))
WORKERS = int(os.environ.get("T45_WORKERS", "4"))
PY = "/Users/aryamahadik/Documents/jev/opendecide-data/.venv/bin/python"


@pytest.fixture(scope="module")
def kit():
    P.warm_cache(workers=WORKERS)
    return P.make_plugin()


def test_contract_and_independence(kit):
    plugin, ctx = kit
    probs = KP.validate_plugin(plugin, strict=True)
    allowed = ("no complement question form", "no non-syntactic complement form", "G0-lite spec is not frozen")
    assert [p for p in probs if not any(a in p for a in allowed)] == [], probs
    assert KP.check_independence(plugin) == []


def test_hermetic_settings():
    assert E.TIMEOUT_S == 5 and E._env()["PYTHONHASHSEED"] == "0"
    assert "http_proxy" not in E._env() and "HTTP_PROXY" not in E._env()
    src = (Path(__file__).parent / "exec_child.py").read_text()
    assert "127.0.0.1" in src and "urllib.request.urlopen" not in src      # the only network is the in-process localhost server


def test_executor_two_runs_and_catalogue(kit):
    for kind in SC.KINDS:
        for fault in SC.KIND_FAULTS[kind]:
            for seed in (0, 1):
                p = SC.exec_params(random.Random(f"cat|{kind}|{fault}|{seed}"), kind, fault)
                res = E.run_exec(kind, p)                      # two independent fresh processes, identical or ExecError
                c = E.classify(res)                            # raises Inconsistent when tag class contradicts retry / repair
                assert c["label"] == SC.FAULT_LABEL[fault], (kind, fault, c)
                assert c["move"] == SC.target_move(fault, p["variant"]), (kind, fault, c)


def test_a_equals_b_and_g3(kit):
    plugin, ctx = kit
    n = max(5, N_AB // 5)
    bad, total, unit_ok = [], 0, 0
    for sampler in P.SAMPLERS:
        for i in range(n):
            spec = plugin.sample(100_000 + i, sampler)
            rr = plugin.render(spec, ctx)
            view = plugin.parse(rr.row, ctx)
            total += 1
            if plugin.solve_b(view) != plugin.solve_a(spec) or plugin.solve_a(spec) != rr.answer:
                bad.append((sampler, i, "A!=B"))
            facts = {k: v for k, v in view.items() if k != "options"}
            if facts != plugin.canonical_for(spec, "T"):
                bad.append((sampler, i, "G3"))
            if view["options"][rr.row["options"].index(rr.row["gold"])] != rr.answer:
                bad.append((sampler, i, "option key"))
    assert total >= min(N_AB, 5 * n) and not bad, bad[:5]
    for i in range(30):                                         # full unit gates (G2 G3 G4 G-SL G-LEX schema) incl. G15
        spec = plugin.sample(200_000 + i, P.SAMPLERS[i % 4])
        res = pipeline.build_unit(plugin, spec, ctx, run_g15=True)
        assert res.ok, res.problems[:3]


def test_solver_b_catches_a_bug(kit):
    plugin, ctx = kit
    spec = plugin.sample(5, "S1")
    row = plugin.render(spec, ctx).row
    view = plugin.parse(row, ctx)
    view2 = {**view, "after": dict(view["before"])}              # the "after" state is replaced by the "before" state
    assert B.solve_b(view2) != B.solve_b(view) or spec.structure["fault"] in ("wrong_target", "busy", "bad_arg", "blocked")


def test_determinism_two_hashseeds(kit):
    code = ("import sys,hashlib,json;sys.path.insert(0,%r);from families.T45 import plugin as P;p,c=P.make_plugin();h=hashlib.sha256();"
            "[h.update(json.dumps(p.render(p.sample(900+i,s),c).row,sort_keys=True).encode()) for i in range(6) for s in ('S1','S2','S3','S4')];"
            "print(h.hexdigest())" % str(C2))
    outs = []
    for hs in ("1", "2"):
        r = subprocess.run([PY, "-B", "-c", code], capture_output=True, text=True, cwd=str(C2),
                           env={**os.environ, "PYTHONHASHSEED": hs}, timeout=900)
        assert r.returncode == 0, r.stderr[-400:]
        outs.append(r.stdout.strip())
    assert outs[0] == outs[1] and len(outs[0]) == 64


def test_heldout_fault_unreachable_by_training_samplers(kit):
    plugin, ctx = kit
    assert SC.HELD_OUT_FAULT not in {f for v in SC.TRAIN_FAULTS.values() for f in v}
    r = AU.heldout_check(plugin, 300)
    assert r["pass"], r
    spec = None
    for s in range(60):
        spec = plugin.sample(300_000 + s, "S5")
        assert plugin.render(spec, ctx).row["meta"]["dev_only"]
        assert plugin.render(spec, ctx).register in TX.HELD_OUT_REGISTERS


def test_surface_names_do_not_move_the_label(kit):
    plugin, ctx = kit
    specs = [plugin.sample(400_000 + i, P.SAMPLERS[i % 4]) for i in range(60)]
    r = AU.name_audit(plugin, specs, 24)
    assert r["pass"] and r["audited"] - r["errors"] >= 12, r      # errors = executions that hit the 5 s cap on a loaded machine


def test_reseed_audit(kit):
    plugin, ctx = kit
    specs = [plugin.sample(500_000 + i, P.SAMPLERS[i % 4]) for i in range(400)]
    r = AU.reseed_audit(plugin, ctx, specs, 0.03)
    assert r["pass"] and r["audited"] >= 12, r


def test_state_has_no_label_words_and_legend_groups(kit):
    plugin, ctx = kit
    words = re.compile("|".join(plugin.LABEL_WORDS), re.I)
    for i in range(300):
        rr = plugin.render(plugin.sample(600_000 + i, P.SAMPLERS[i % 5]), ctx)
        assert not words.search(rr.row["state"]), rr.row["state"]
    for L in range(TX.N_LEGENDS):
        leg = TX.legend_of(L)
        row = {"instructions": "\n".join(TX.legend_lines(L))}
        got = {c: g for c, g in B.LEGEND_LINE.findall(row["instructions"])}
        assert len(got) == 4
        for g in "TAH0":
            text = TX.GROUP_TEXT[g][leg["phr"][g]]
            hits = [x for x, rx in B.GROUP_WORDS if re.search(rx, text)]
            assert hits == [g], (L, g, text, hits)


def test_shown_set_design_is_label_blind():
    from collections import Counter
    for qform, anchor, n_lab in (("ch_outcome", "SUCCESS", 6), ("ch_move", "ADVANCE", 4)):
        c, k2, n = Counter(), 0, 6000
        for i in range(n):
            shown, gold = P.shown_set(f"x|{i}|{qform}", qform)
            assert anchor in shown and gold in shown and len(set(shown)) == len(shown)
            c[gold] += 1
            k2 += len(shown) == 2
        exp = k2 / n / 2 + (1 - k2 / n) / 3
        assert abs(c[anchor] / n - exp) < 0.02
        assert qform != "ch_outcome" or c[anchor] / n >= 0.35
        assert all(c[l] > 0 for l in (TX.LABELS if qform == "ch_outcome" else TX.MOVES))


def test_prompt_budget_and_cards(kit):
    plugin, ctx = kit
    toks, cards = [], {}
    for i in range(300):
        rr = plugin.render(plugin.sample(700_000 + i, P.SAMPLERS[i % 4]), ctx)
        toks.append(approx_tokens(rr.row))
        cards[rr.row["meta"]["card_id"]] = cards.get(rr.row["meta"]["card_id"], 0) + 1
    assert sum(toks) / len(toks) <= 1200 and max(toks) <= 2000          # 3-chars-per-token estimate; the real tokenizer runs in prefreeze.py
    assert max(cards.values()) <= 64


def test_in_memory_build(kit):
    import pilot
    import pilot_loaders as PL
    from families.T45 import run_pilot_i1 as RUN
    PL.LOADERS["T45"] = RUN._t45
    RUN.install_patches()
    with PL.LOADERS["T45"]() as k:
        b = pilot.build_pilot(k, BUILD_N, run_g15=False)
    assert b.stats["reached_target"] and not b.stats["drops_by_gate"], b.stats["drops_by_gate"]
    sets = [rr.option_set for u in b.units for rr in u.rendered if rr.option_set is not None]
    assert len(sets) >= BUILD_N
    pr = plan_report(sets)
    assert pr.get("pass", True), pr
