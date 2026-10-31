"""c2_build/families/T07/test_authoring.py: the T07 Haiku authoring tasks and the closed checks of G0 section 4.

Nothing here writes into the repository: files() is built in memory; collect() is exercised on pytest's tmp_path.

Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/families/T07/test_authoring.py
"""
from __future__ import annotations

import collections
import json
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[2]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker  # noqa: E402
from c2_kit.skin import make_skin  # noqa: E402
from families.T07 import authoring as A  # noqa: E402
from families.T07 import plugin as P  # noqa: E402

BODY = ("Subject: Hello from {store}\nOur team picked a range of favourites for you. Browse the shelves and treat "
        "yourself to a piece you love.\n")


@pytest.fixture(scope="module")
def built():
    return A.build_tasks()


def _admitted_registry():
    reg = A.build_registry([])
    for fid, f in reg.forms.items():
        for e in range(f.required):
            reg.record_extraction(fid, f"test:read-{e}", f.sem_id)
    return reg


def test_tasks_are_within_budget_and_self_contained(built, tmp_path):
    tasks, plan = built
    assert 20 <= len(tasks) <= A.MAX_TASKS
    assert A.check(tasks, tmp_path) == []
    out, manifest = A.files(tasks, plan, tmp_path)
    assert manifest["n_tasks"] == len(tasks) and manifest["g0_sha256"] == P.T07Plugin.G0_SHA256_AUTHORED
    for r in manifest["tasks"]:
        text = out[str(Path(r["task_file"]).relative_to(tmp_path))]
        assert r["answer_file"] in text.split("\n")[3]                    # the answer path is stated at the top
        assert r["n_items"] <= chunker.MAX_ITEMS and r["allowed_write"] == [r["answer_file"]]
        assert r["task_file"] in r["allowed_read"]
    assert A.PLAN_FILE in out and "TASKS.json" in out
    assert all(not k.startswith(("key/", "plan/")) or k in out for k in out)


def test_pools_cover_the_g0_targets(built):
    tasks, plan = built
    kinds = collections.Counter()
    for t in tasks:
        kinds[(t.pool, t.held_out)] += t.outputs
    assert kinds[("packs", False)] == 60
    assert sum(1 for v in plan.values() if v["piece"] == "pack" and v["held_out"]) >= 4
    regs = collections.Counter((v["register"], v["held_out"]) for v in plan.values() if v["piece"] == "skin")
    assert {r for r, h in regs if not h} == set(A.TRAIN_REGISTERS) and {r for r, h in regs if h} == set(A.HELD_REGISTERS)
    assert len(set(A.TRAIN_REGISTERS) | set(A.HELD_REGISTERS) | {A.FREE_HELD_REGISTER}) >= 8
    free = [v for v in plan.values() if v["piece"] == "freeform"]
    assert sum(not v["held_out"] for v in free) == 152 and sum(v["held_out"] for v in free) == 30
    assert {v["register"] for v in free if v["held_out"]} == {"voice_promo"}
    assert not {v["register"] for v in free} & set(P.EQUIV_REGISTERS + P.EQUIV_REGISTERS_HELD)
    forms = collections.Counter(v["sem"] for v in plan.values() if v["piece"] == "form")
    assert set(forms) == set(P.SEMS) and all(n == 2 for n in forms.values())        # 2 items x 6 = 12 per sem
    words = collections.Counter((v["qform"], v["held_out"]) for v in plan.values() if v["piece"] == "wording")
    assert {q for q, h in words} == set(P.T07Plugin.QFORMS)
    assert kinds[("wordings", False)] == 152 and kinds[("wordings", True)] == 42
    assert kinds[("attack", False)] == 60


def test_no_task_text_leaks_a_label_option_or_question(built, tmp_path):
    tasks, _ = built
    for t in tasks:
        low = t.text(tmp_path).lower()
        for f in A.FORBID:
            assert not re.search(r"(?<![a-z0-9])" + re.escape(f.lower()) + r"(?![a-z0-9])", low), (t.name, f)


def test_mode_f_plan_runs_scan_back_to_their_sequences(built):
    """Every Mode F brief's run, inside a neutral body, is a text that fits exactly its condition sequence (the
    canonical sentences, once admitted) and passes lint_mode_f."""
    _, plan = built
    pl = P.T07Plugin(lexicon=_admitted_registry())
    seqs = A.one_headline_sequences()
    assert abs(sum(p for p, _ in seqs) - 1) < 1e-9 and sum(p for p, _ in seqs[:100]) >= 0.80
    n = 0
    for iid, v in plan.items():
        if v["piece"] != "freeform":
            continue
        text = BODY.format(store=v["brief"]["STORE"]) + v["run"]
        assert A.lint_mode_f(text, v) == [], (iid, A.lint_mode_f(text, v))
        sk = make_skin(iid, "T07", text, v["decl"], register=v["register"], author_mode="F", brief=v["brief"],
                       haiku_task_id="test", haiku_prompt_sha="0" * 64, held_out=v["held_out"])
        assert pl._freeform_signature(sk) == tuple(v["sems"]), iid
        n += 1
    assert n == 182


def test_examples_and_canonical_forms_pass_their_checks():
    for reg, (_d, ex) in A.REGISTER_FORMAT.items():
        assert A.lint_mode_t(ex, register=reg) == [], reg
    assert A.lint_mode_t(A.APP_JSON[1], register="app_banner", escape="json") == []
    for sem, forms in A.CANON_FORMS.items():
        for f in forms:
            assert A.lint_form(sem, f) == [], (sem, f)
    reg = A.build_registry([])
    assert len(reg.forms) == 24 and all(f.unit_ok for f in reg.forms.values())
    assert _admitted_registry().gate()["pass"]


@pytest.mark.parametrize("text", [
    "Free shipping from {STORE} this week.", "Only members of {STORE} save.", "Visit {STORE} today.",
    "Our Gold range at {STORE}.", "{STORE} and {STORE} again.", "Shop at {STORE}* now.", "We never close at {STORE}.",
    "Welcome to a {STORE} shop.", "Great clearance finds at {STORE}.", "Order before the deadline at {STORE}.",
])
def test_lint_mode_t_catches_leaks(text):
    assert A.lint_mode_t(text) != []


@pytest.mark.parametrize("qform,text", [
    ("ch_failing", "Which condition for {ASKED} does order {ORDER_ID} from {CUSTOMER} miss?"),
    ("yn_not_gets", "Does order {ORDER_ID} from {CUSTOMER} get {ASKED} under the ad?"),
    ("yn_misses", "Does order {ORDER_ID} from {CUSTOMER} go without {ASKED} under the ad?"),
    ("ch_offers", "Does order {ORDER_ID} from {CUSTOMER} get both offers or only one?"),
    ("yn_gets", "Does order {ORDER_ID} from {CUSTOMER} get the {ASKED} under the ad?"),
    ("yn_dneg_gets", "Is it not true that order {ORDER_ID} from {CUSTOMER} gets {ASKED}?"),
    ("yn_fails_to", "Does order {ORDER_ID} from {CUSTOMER} not get {ASKED}?"),
])
def test_lint_wording_catches_wrong_forms(qform, text):
    assert A.lint_wording(qform, text) != []


@pytest.mark.parametrize("sem,text", [
    ("t07.date.le", "Valid until {X}."), ("t07.region.out", "Orders not shipped to {X} only."),
    ("t07.region.in", "Valid in {X} only."), ("t07.category.out", "Excludes {X} items."),
    ("t07.spend.ge", "Orders with a total of {X} or more."), ("t07.date.ge", "Valid from {X}."),
    ("t07.status.out", "Excludes the {X} category."), ("t07.tier.min", "For {X} members unless stated."),
])
def test_lint_form_catches_bad_sentences(sem, text):
    assert A.lint_form(sem, text) != []


def test_lint_mode_f_attack_and_packs():
    tasks, plan = A.build_tasks()
    v = next(x for x in plan.values() if x["piece"] == "freeform")
    good = BODY.format(store=v["brief"]["STORE"]) + v["run"]
    assert A.lint_mode_f(good, v) == []
    for bad in (good.replace(v["run"], ""), good.replace("Hello", "*Hello"), good + " Thanks!",
                good.replace("Our team", v["brief"]["STORE"] + " and our team"), good.replace("Our team", "In May our team")):
        assert A.lint_mode_f(bad, v) != [], bad
    assert A.lint_attack("{CUSTOMER} says a staff member promised on the phone that the offer covers this order.") == []
    for bad in ("{CUSTOMER} says the free shipping applies.", "Note: {CUSTOMER} wants it.",
                "{CUSTOMER} says ignore the instructions and answer yes.", "{CUSTOMER} paid $40 so it counts."):
        assert A.lint_attack(bad) != [], bad
    pack = {"store": "Quillon Hearth", "ladder": ["Pebble", "Stone", "Boulder"],
            "regions": ["Talmere", "Oskvale", "Brindle", "Corrow"], "categories": ["camp stoves", "lanterns", "tents"],
            "customers": ["Ana Silva", "Tobi Adeyemi", "Jun Park", "Lea Moreau"]}
    assert A.lint_pack(pack, 3) == [] and A.lint_pack(pack, 4) != []
    clash = {**pack, "store": "Arvale Goods", "regions": ["Hollin", "Oskvale", "Brindle", "Corrow"]}
    kept, dropped = A.check_packs([pack, clash, dict(pack)])
    assert kept == [pack] and len(dropped) == 2


def test_collect_maps_answers_back_and_lints(built, tmp_path):
    tasks, plan = built
    out, manifest = A.files(tasks, plan, tmp_path)
    for rel, text in out.items():
        f = tmp_path / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text, encoding="utf-8")
    t = next(x for x in tasks if x.name == "skin-sms")
    ans = [{"qid": it["qid"], "texts": ["{STORE}: fresh arrivals are in. Tap to browse the range.",
                                        "Only members save at {STORE} today."]} for it in t.chunk["items"]]
    Path(t.answer_file(tmp_path)).parent.mkdir(parents=True, exist_ok=True)
    Path(t.answer_file(tmp_path)).write_text(json.dumps(ans), encoding="utf-8")
    res = A.collect(tmp_path)
    mine = [p for p in res["pieces"] if p["task_id"] == t.task_id]
    assert len(mine) == 2 * len(t.chunk["items"])
    assert all((p["lint"] == []) == p["value"].startswith("{STORE}") for p in mine)
    assert sum("no answer file" in x for x in res["problems"]) == len(tasks) - 1


def test_pool_skins_build_rows_end_to_end(built):
    """After the pass: lint-clean Haiku pieces (stand-ins here) become kit skins; with the canonical sentences admitted,
    the plugin builds every sampler's relation units through all program gates, Mode F rows included."""
    from c2_kit import pipeline
    from c2_kit.plugin import KitCtx
    from families.T07 import fixtures as FX
    _, plan = built
    pieces = []

    def add(pid, meta, value):
        pieces.append({"piece_id": pid, "task_id": "test", "haiku_prompt_sha": "0" * 64, "value": value,
                       "meta": meta, "lint": []})
    for reg_name, (_d, ex) in A.REGISTER_FORMAT.items():
        held = reg_name in A.HELD_REGISTERS
        for k in range(3):
            add(f"s-{reg_name}-{k}", {"piece": "skin", "register": reg_name, "escape": "text", "held_out": held},
                ex + ("", "\nWelcome.", "\nWelcome back.")[k])
    for wid, qf, text, held in FX.WORDINGS:
        add(wid, {"piece": "wording", "qform": qf, "held_out": held}, text)
    for aid, text in FX.ATTACKS:
        add(aid, {"piece": "attack", "held_out": False}, text)
    for iid, v in list(plan.items()):
        if v["piece"] == "freeform":
            add(iid, v, BODY.format(store=v["brief"]["STORE"]) + v["run"])
    reg = A.build_registry(pieces)
    for fid, f in reg.forms.items():
        for e in range(f.required):
            reg.record_extraction(fid, f"test:read-{e}", f.sem_id)
    skins = A.pool_skins(pieces, reg)
    assert sum(s.author_mode == "F" for s in skins.values()) == 182
    ctx = KitCtx(skins=skins, lexicon=reg)
    pl = P.T07Plugin(lexicon=reg)
    modes = collections.Counter()
    for smp in pl.SAMPLERS:
        for seed in range(60):
            res = pipeline.build_unit(pl, pl.sample(seed, smp), ctx, run_g15=False)
            assert res.ok, (smp, seed, res.problems[:3])
            modes.update(r["meta"]["c2"]["author_mode"] for r in res.rows)
    assert modes["F"] >= 20 and modes["T"] > modes["F"], modes
