"""families/T07/haiku/redo2/test_build_redo2.py: the T07 redo2 author tasks and the R1-R5 fixes (G0_SPEC.md section 7).

Everything is built in memory; nothing is written. Run (from lean/):
  ../.venv/bin/python -m pytest -q c2_build/families/T07/haiku/redo2/test_build_redo2.py
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[4]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from c2_kit import chunker  # noqa: E402
from c2_kit import slots as S  # noqa: E402
from families.T07 import authoring as A  # noqa: E402
from families.T07 import plugin as P  # noqa: E402
from families.T07.haiku.redo2 import build_redo2 as R  # noqa: E402


@pytest.fixture(scope="module")
def built():
    return R.author_files()


@pytest.fixture(scope="module")
def batches():
    return R.build_batches()


@pytest.fixture(scope="module")
def reg_r1():
    drops = []
    reg, origin = R.build_registry([], drops)          # v1 forms + the R1 pair; stops if a v1 status changes
    assert drops == []
    return reg, origin


def test_author_tasks_are_ready_and_self_contained(built):
    files, index = built
    assert R.check_author(files) == []
    assert index["n_tasks"] == len(index["tasks"]) <= 40
    for r in index["tasks"]:
        text = files[str(Path(r["task_file"]).relative_to(R.ROOT))]
        assert text.split("\n")[3] == r["answer_file"] and r["allowed_write"] == [r["answer_file"]]
        assert r["task_file"] in r["allowed_read"] and r["n_items"] <= chunker.MAX_ITEMS
        assert "ANSWER CONTRACT" in text and f"outputs expected: {r['outputs_expected']}" in text
        assert "/redo2/answers/" in r["answer_file"] and "/haiku/author/" not in r["answer_file"]


def test_pack_words_are_the_frozen_ones():
    res = A.collect()
    assert R.PACK_WORDS == A.pack_words(res["packs_kept"]) and len(R.PACK_WORDS) == 587


def test_asks_cover_every_v1_deficit(batches):
    d = R.deficits()
    assert d[("skin", "catalogue")] == 16 and d[("attack",)] == 10
    assert d[("wording", "yn_misses", "training")] == 8 and d[("wording", "yn_misses", "held_out")] == 3
    assert d[("form", R.STATUS)] == 1 and d[("form", "t07.tier.max")] == 1 and d[("canonical", R.STATUS)] == 2
    _b, plan, _s = batches["freeform"]
    briefs = {m["v1_brief"] for m in plan.values()}
    assert len(briefs) == 151 and not briefs & R.v1_admitted_briefs()
    assert all(sum(1 for m in plan.values() if m["v1_brief"] == b) == R.FREE_CANDIDATES for b in briefs)


# ------------------------------------------------------------------------------------------------ R1
def test_r1_v1_diagnosis_and_new_pair(reg_r1):
    reg, origin = reg_r1
    v1 = [f for f, x in reg.forms.items() if x.text in A.CANON_FORMS[R.STATUS]]
    assert len(v1) == 2 and all(reg.status(f) == "rejected" for f in v1)            # stays rejected (H32)
    assert reg.lexicon_items(v1)[0][1]["text"] in ("Excludes production items.", "Items sold as production are excluded.")
    new = [f for f, o in origin.items() if o["origin"] == "canonical_r2"]
    assert sorted(reg.forms[f].text for f in new) == sorted(R.CANON_STATUS_R2)
    for f in new:
        assert reg.forms[f].unit_ok and reg.status(f) == "pending"
        assert A.lint_form(R.STATUS, reg.forms[f].text, R.PACK_WORDS) == []
        txt = reg.render(f, R.read_values(reg, f))
        assert "production" not in txt and any(s[0] in txt for k, s in P.STATUSES.items() if k != "regular_price")


def test_r1_read_values_take_the_forms_own_dimension(reg_r1):
    reg, _origin = reg_r1
    seen_dims = set()
    for fid, f in sorted(reg.forms.items()):
        vals = R.read_values(reg, fid)
        if f.kind == "question":
            assert vals["ORDER_ID"].value.startswith("ORD-") and vals["CUSTOMER"].value in P.CUSTOMERS
            if "ASKED" in vals:
                assert vals["ASKED"].value in P.BENEFITS
            continue
        dim, op = P.SEMS[f.sem_id][:2]
        seen_dims.add(dim)
        v = vals["X"].value
        if dim in P.CAT_SET:
            assert v in P.CAT_SET[dim] and v != "regular_price"
        if dim == "tier":
            lad = next(x for x in P.LADDERS if v in x)
            assert (lad.index(v) > 0) if op == "min" else (lad.index(v) < len(lad) - 1)
        assert R.lex_items(reg, [fid], "redo2-r1")[0][1]["text"] == R.lex_items(reg, [fid], "redo2-r2")[0][1]["text"]
    assert seen_dims == set(P.DIMS)


def test_r1_mode_f_status_briefs(batches):
    _b, plan, _s = batches["freeform"]
    v1 = R.v1_plan()
    status = [m for m in plan.values() if R.STATUS in m["sems"]]
    assert len(status) == 46 * R.FREE_CANDIDATES
    for m in plan.values():
        if R.STATUS in m["sems"]:
            assert set(m["canon_forms"]) & set(R.CANON_STATUS_R2)
            assert not set(m["canon_forms"]) & set(A.CANON_FORMS[R.STATUS])
            assert A.lint_form(R.STATUS, next(f for f in m["canon_forms"] if f in R.CANON_STATUS_R2)) == []
        else:
            assert (m["run"], m["canon_forms"]) == (v1[m["v1_brief"]]["run"], v1[m["v1_brief"]]["canon_forms"])
        assert m["brief"] == v1[m["v1_brief"]]["brief"] and m["register"] == v1[m["v1_brief"]]["register"]


# ------------------------------------------------------------------------------------------------ R2
def test_r2_yn_misses_brief(batches):
    assert "lose out on" in R.YN_MISSES_R2 and "forfeit" in R.YN_MISSES_R2
    assert not re.search(r"go short|shut out", R.YN_MISSES_R2)
    assert R.YN_MISSES_R2 != A.Q_MEANING["yn_misses"] and A.Q_SEM_MEANING["yn_misses"].startswith(
        "asks whether the customer's order loses out on")                           # meaning list unchanged
    b, plan, _s = batches["wordings"]
    for c in b.chunks:
        for it in c["items"]:
            m = plan[b.key[it["qid"]]]
            if m["held_out"]:
                assert "advertis" not in it["brief"]["meaning"] and it["brief"]["style"] == A.HELD_STYLE


# ------------------------------------------------------------------------------------------------ R3
def test_r3_every_prompt_lists_the_pack_words(batches):
    pw = sorted(w for w in R.PACK_WORDS if not A._bad(w))
    for name, (b, _plan, _s) in batches.items():
        words = set(A._words(b.prompt))
        assert [w for w in pw if w not in words] == [], name
    # the v1 drop is still a drop: the gate is unchanged, only the prompt knows the words now
    assert A.lint_mode_t("Bright ideas for every room live at {STORE}.", extra=R.PACK_WORDS)


# ------------------------------------------------------------------------------------------------ R4
def test_r4_frames_and_examples_pass_lint_without_label_words(batches):
    for sem, exs in R.FORM_EXAMPLES.items():
        for t in exs:
            assert A.lint_form(sem, t, R.PACK_WORDS) == [], t
    for t in ("Applies to members ranked {X} or lower.", "Limited to members at {X} level and below.",
              "Restricted to {X} members and below.", "Stock priced as {X} sits outside this offer."):
        sem = R.STATUS if "priced" in t else "t07.tier.max"
        assert A.lint_form(sem, t, R.PACK_WORDS) == [], t
    for name, (b, _plan, _s) in batches.items():
        low = b.prompt.lower()
        assert not [w for w in P.T07Plugin.LABEL_WORDS if re.search(r"(?<![a-z0-9])" + w + r"(?![a-z0-9])", low)]
    assert A.lint_form("t07.tier.max", "Members ranked {X} or lower qualify.") == ["label word"]   # gate unchanged


# ------------------------------------------------------------------------------------------------ R5
def test_r5_lint_unchanged_prompt_says_so():
    assert A.lint_form("t07.region.out", "Shipping to {X} falls outside this offer.") == ["promise word ['shipping']"]
    assert A.lint_form(R.STATUS, "Goods whose price status is {X} fall outside the headline offer.") == \
        ["names a value ['price']"]
    assert A.lint_form("t07.region.out", "Orders shipped to {X} are excluded.", R.PACK_WORDS) == []
    assert '(never "shipping")' in R.FORM_PROMPT and 'never the word "price"' in R.FORM_PROMPT


# ------------------------------------------------------------------------------------------------ admit helpers, G0
def test_one_text_per_brief_is_label_blind():
    kept, spare = R.pick_one_per_brief([("b1", 1, "p1b", True), ("b1", 0, "p1a", True), ("b2", 0, "p2a", False),
                                        ("b2", 1, "p2b", True), ("b3", 0, "p3a", False), ("b3", 1, "p3b", False)])
    assert kept == {"b1": "p1a", "b2": "p2b"} and spare == ["p1b"]


def test_g0_is_repinned_with_section_7():
    text = P.HERE.joinpath("G0_SPEC.md").read_text(encoding="utf-8")
    assert hashlib.sha256(text.encode()).hexdigest() == P.T07Plugin.G0_SHA256_AUTHORED
    assert len(text.splitlines()) <= 200 and "## 7. Redo2 notes" in text
    assert all(re.search(rf"^R{i} ", text, re.M) for i in range(1, 6))
    assert all(t in " ".join(text.split()) for t in R.CANON_STATUS_R2)


def test_slot_kinds_unchanged():
    assert P.BOUND_KIND["status"] == "category" and S.sample_slots("category")[0].value == "prod"
