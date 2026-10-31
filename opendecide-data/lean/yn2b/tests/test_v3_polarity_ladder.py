"""F4 decide2 (golden_src/gen3/v3_polarity_ladder.py, builder C): independence from the generator, the frame lexicon,
the proposition forms, the truth routes, and the WRITTEN rows (SPEC 8.1 agreement 100%, 8.3 structure, the second
route through the source rows, meta cross-checks, wording probes, label swaps). Read-only: no test writes outside
pytest's tmp_path (the manifest is redirected by conftest)."""
from __future__ import annotations

import ast
import inspect
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
GEN3 = LEAN / "golden_src" / "gen3"
for p in (str(GEN3), str(LEAN / "yn2b")):
    if p not in sys.path:
        sys.path.insert(0, p)

import mv_core as mv  # noqa: E402
import v3_polarity_ladder as v  # noqa: E402

MOD = GEN3 / "v3_polarity_ladder.py"
TEMPLATES = LEAN / "yn2b" / "f4_templates.json"
WRITTEN = (v.RAW / f"{v.KEY}.jsonl").exists() and (v.RAW / "dev" / f"{v.KEY}.jsonl").exists()
needs_rows = pytest.mark.skipif(not WRITTEN, reason="F4 raw rows not written")
P_MAY = "the proposed call may run under the policy"


# ================================================================================================ independence
def test_module_never_imports_the_generator():
    tree = ast.parse(MOD.read_text())
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names |= {a.name.split(".")[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call) and getattr(node.func, "id", None) == "_v3" and node.args and \
                isinstance(node.args[0], ast.Constant):
            names.add(node.args[0].value)
    assert not names & set(v.FORBIDDEN_IMPORTS), names
    dynamic = {n for n in names if n.startswith("v3_")}
    assert dynamic <= {"v3_rule_chain", "v3_tool_guard", "v3_state_track", "v3_def_literal"}, dynamic


SOLVER_FUNCS = ("solve", "decide2_row", "parse_frame", "_frame_hit", "classify_p", "f3_statement", "card_of",
                "card_parts", "_shown", "truth", "truth_a", "truth_b", "golden_row", "prefetch_golden")


def test_solver_reads_no_gold_no_build_record_and_few_meta_keys():
    meta_keys = set()
    for name in SOLVER_FUNCS:
        src = inspect.getsource(getattr(v, name))
        for bad in ("SOURCES", "f4_sources", "f4_templates", "flips\"]", 'row["gold"]', "row.get(\"gold\")",
                    "polarity", "\"tpl\"", "renderer", "\"role\"", "\"view\"", "\"tier\"", "truth\"]"):
            if bad == 'truth"]' and name in ("solve",):
                continue  # solve reads its own truth dict
            assert bad not in src, (name, bad)
        meta_keys |= set(re.findall(r"""meta"\)? or \{\}\)\.get\("(\w+)"\)""", src))
        meta_keys |= set(re.findall(r"""\["meta"\]\["(\w+)"\]""", src))
    assert meta_keys <= {"defs", "card_style", "derived_from", "fmt"}, meta_keys


# ================================================================================================ the frame lexicon
def _templates():
    return [t["text"] for t in json.loads(TEMPLATES.read_text())]  # text only; the `flips` field is never read


@pytest.mark.skipif(not TEMPLATES.exists(), reason="F4 templates not written")
def test_every_frame_text_parses_to_one_frame_with_a_full_ladder():
    by = defaultdict(list)
    used = defaultdict(set)
    for t in _templates():
        fr = v.parse_frame(t.replace("{d}", P_MAY))
        assert fr.d == P_MAY
        by[fr.name].append(fr.flips)
        for k, w in fr.switches.items():
            used[fr.name].add((k, w))
        if fr.inner:
            used[fr.name].add(("inner", fr.inner))
    assert set(by) == {n for n, _ in v.FRAMES}, {n for n, _ in v.FRAMES} ^ set(by)
    for name, fl in by.items():
        assert sorted(fl) == [0, 1, 1, 2], (name, fl)  # SPEC 5 F4: para, negA, negB, dneg
    # every wording of every switch slot occurs in some frame text (no dead lexicon entry)
    for name, rx, signs in v.COMPILED:
        for sw, words in signs.items():
            assert {w for w in words} <= {w for k, w in used[name] if k == sw}, (name, sw)


@pytest.mark.parametrize("neg", v.NEG_INNER)
def test_each_inner_negation_is_one_flip(neg):
    base = v.parse_frame(f"Going by the material given, is it established that {P_MAY}?")
    fr = v.parse_frame(f"Going by the material given, is it established that {neg} {P_MAY}?")
    assert (base.flips, fr.flips, fr.inner, fr.d) == (0, 1, neg, P_MAY)


def test_switch_polarity_reads_like_english():
    cases = {
        "A gate is meant to admit an item exactly when {d}. If the gate turned away this item, did it act improperly?": 2,
        "A rule lets a case proceed exactly when {d}. Given the material provided, would it be proper to stop this case?": 1,
        "Would someone who denied that {d} have to give up that view after studying the information supplied?": 2,
        "The compliance tracker marks the requirement that {d} as unmet. Does the material given support that marking?": 1,
        "Does the material given fall short of the burden of showing that it does not hold that {d}?": 2,
        "One checklist item says that {d}. Going by the material given, should that item be ticked as not done?": 1,
        "Read strictly, does the material given deny that it cannot be said that {d}?": 2,
        "Is the conclusion that {d} carried by the material given?": 0,
    }
    for t, n in cases.items():
        assert v.parse_frame(t.replace("{d}", P_MAY)).flips == n, t


def test_unknown_or_stacked_wording_is_undefined():
    for q in (f"Is it the case that {P_MAY}?",
              f"Going by the material given, is it established that it does not hold that it is untrue that {P_MAY}?",
              f"Going by the material given, is it probable that {P_MAY}?"):
        with pytest.raises(v.ParseError):
            v.parse_frame(q)
        assert v.decide2_row({"instructions": q, "options": ["yes", "no"], "state": "", "meta": {}}) is v.UNDEFINED


def test_non_yes_no_row_is_undefined():
    q = f"Going by the material given, is it established that {P_MAY}?"
    assert v.decide2_row({"instructions": q, "options": ["a", "b"], "state": "", "meta": {}}) is v.UNDEFINED


# ================================================================================================ propositions
P_CASES = [
    ('"animosity" is the listed description that fits this post best', "a", None),
    ('"EFU (unrated)" is the listed EF rating that fits this storm survey best', "a", None),
    ('the outcome of this coverage request under the formulary is "covered in full"', "f1.outcome",
     'Under the formulary, is the outcome of this coverage request "covered in full"?'),
    ("the decision recorded in the case file for this leave request is consistent with the handbook", "f1.record",
     "Is the decision recorded for this leave request in line with the handbook, rather than at odds with it?"),
    ("under the rules in the card, the evidence establishes the claim", "f1b.claim",
     "Under the rules in the card, does the evidence establish the claim?"),
    ("under the card's rules, the fact-check log entry for this claim is consistent with the evidence", "f1b.log",
     "The fact-check log has an entry for this claim. Is that entry consistent with the evidence under the card's "
     "rules, rather than at odds with it?"),
    (P_MAY, "f2.may", "Is the proposed call allowed to run under the policy?"),
    ("the verdict the guardrail logged for the proposed call is consistent with the policy", "f2.verdict",
     "Is the verdict the guardrail logged for the proposed call consistent with the policy?"),
    ("the assistant's output meets every requirement stated for it", "f2.output",
     "Is every stated requirement met by the assistant's output?"),
    ("every value in the agent record is supported by the log and the numbered rules", "f3.record",
     "Is every value in the agent record supported by the log and the numbered rules?"),
    ("order SO-4342750 is in status paid at the end of the log", "f3.state",
     "Order SO-4342750 is in status paid at the end of the log."),
    ("plan-4467.pdf is in the reports folder at the end of the session", "f3.state",
     "plan-4467.pdf is in the reports folder at the end of the session."),
    ("Siva Goltard can edit RES-3742206 at 2026-04-07T13:19:00Z", "f3.state",
     "Siva Goltard can edit RES-3742206 at 2026-04-07T13:19:00Z."),
    ("the cart holds at least 3 of SKU-292202 at 2026-04-17T10:50:00Z", "f3.state",
     "The cart holds at least 3 of SKU-292202 at 2026-04-17T10:50:00Z."),
    ("the consignment is a 'nut' under Tariff Note 26 of the Harbour Tariff Schedule", "f6.term",
     "Under Tariff Note 26 of the Harbour Tariff Schedule, is the consignment a 'nut'?"),
    ("the bid is a 'small business' by the definition in Rule 20, not by everyday usage", "f6.term",
     "Going by the definition in Rule 20 and not by everyday usage, is the bid a 'small business'?"),
    ("the absence qualifies as a 'holiday' under the definition in Section 20 alone", "f6.term",
     "Applying only the definition in Section 20, with no outside rules, does the absence qualify as a 'holiday'?"),
    ("Rule 3 supports the classification the league eligibility register records for the player", "f6.record",
     "Does Rule 3 support the classification the league eligibility register records for the player?"),
    ("the classification on file for the bid is consistent with the definition in Rule 4", "f6.record",
     "Under Rule 4, is the classification on file for the bid consistent with the definition?"),
]


@pytest.mark.parametrize("p,kind,q", P_CASES)
def test_classify_p(p, kind, q):
    pr = v.classify_p(p)
    assert pr.kind == kind and pr.question == q


def test_unknown_proposition_raises():
    for p in ("the moon is made of cheese", "the proposed call must be blocked under the policy"):
        with pytest.raises(v.ParseError):
            v.classify_p(p)


def test_card_parts_order_is_enforced():
    good = {"task": "t", "x": "1", "y": "2", v.HOLDS: "h", v.FAILS: "f", "yes": "Y", "no": "N"}
    p = v.card_parts(good)
    assert (p["task"], list(p["extra"]), p["holds"], p["fails"]) == ("t", ["x", "y"], "h", "f")
    with pytest.raises(v.ParseError):
        v.card_parts({"yes": "Y", "no": "N", v.HOLDS: "h", v.FAILS: "f"})


# ================================================================================================ written rows
@pytest.fixture(scope="module")
def parts():
    out = {}
    for part in ("train", "dev"):
        rows = v.load_rows(part)
        out[part] = (rows, v.load_rels(part), v.agreement(rows))
    return out


@needs_rows
def test_counts(parts):
    tr, dev = parts["train"][0], parts["dev"][0]
    assert len(tr) == 1500 and len(dev) == 300
    assert Counter(r["meta"]["dev_kind"] for r in dev) == {"iid": 150, "holdout": 150}


@needs_rows
def test_agreement_is_100_percent(parts):
    for part, (rows, _, ag) in parts.items():
        assert ag["agree"] == ag["rows"] == len(rows), (part, ag["disagreements"][:5])


@needs_rows
def test_official_verify_labels(parts):
    for part, (rows, _, _) in parts.items():
        rep = mv.verify_labels(rows, v.decide2_row)
        assert rep["ok"] and rep["rows"] == len(rows), (part, rep)


@needs_rows
def test_structure_under_decide2(parts):
    for part, (rows, rels, ag) in parts.items():
        st = v.structure_under_decide2(rows, rels, ag["answers"])
        # every relation of the written file is checked (the counts follow the build: R2's rebuild has 379 / 371
        # train and 81 / 69 dev complement / equiv relations; the first build had 375 / 375 and 76 / 74)
        want = Counter(rel["type"] for rel in rels)
        assert (st["complement"], st["equiv"]) == (want["complement"], want["equiv"]), (part, st)
        assert st["complement"] + st["equiv"] == len(rows) // 2, part
        assert not st["complement_not_inverted"] and not st["equiv_changed"], part
        assert not st["unknown_rel"] and not st["same_state_broken"], part


@needs_rows
def test_meta_crosscheck_is_clean(parts):
    for part, (rows, _, ag) in parts.items():
        mc = v.meta_crosscheck(rows, ag["infos"])
        for k in ("polarity", "role", "view", "renderer", "P_vs_sources", "derived_from",
                  "held_out_frame_outside_holdout", "holdout_with_training_frame"):
            assert not mc[k], (part, k, mc[k][:3])
    fams = v.meta_crosscheck(parts["dev"][0], parts["dev"][2]["infos"])["frame_family_by_split"]
    assert set(fams["holdout"]) == set(v.HELD_OUT_FAMILIES)


@needs_rows
def test_second_route_through_the_source_rows(parts):
    for part, (rows, _, ag) in parts.items():
        sc = v.source_crosscheck(rows, ag["infos"])
        assert sc["b_rows"] == sum(1 for i in ag["infos"].values() if i["kind"] != "a")
        assert sc["route2_agree"] == sc["b_rows"], (part, sc["route2_disagree"][:3], sc["route2_undefined"][:3])
        for k in ("state_not_copied", "extra_lines_not_copied", "holds_fails_not_source_yes_no",
                  "source_gold_vs_route1", "missing_source"):
            assert not sc[k], (part, k, sc[k][:3])


@needs_rows
def test_cards_say_what_the_question_asks(parts):
    for part, (rows, _, ag) in parts.items():
        cd = v.card_report(rows, ag["infos"])
        assert cd["rows"] == len(rows)
        for k, x in cd.items():
            if k != "rows":
                assert not x, (part, k, x[:3])


@needs_rows
def test_every_wording_probe_moves_the_answer(parts):
    for part, (rows, _, ag) in parts.items():
        s = v.sensitivity(rows, ag["answers"])
        assert s["probes"] >= 3 * len(rows) and s["ok"] == s["probes"], (part, s["failed"][:5])


STRIP = ("polarity", "role", "view", "tpl", "renderer", "tier", "latent_id", "edge", "shortcut_hits",
         "n_shortcut_wrong", "judge", "pack", "twin_of", "dev_kind")


@needs_rows
def test_decide2_ignores_gold_and_label_bearing_meta(parts):
    for part, (rows, _, ag) in parts.items():
        for r in rows:
            meta = {k: x for k, x in r["meta"].items() if k not in STRIP}
            blind = {**{k: x for k, x in r.items() if k not in ("gold", "soft")}, "meta": meta}
            assert v.decide2_row(blind) == ag["answers"][r["rid"]], r["rid"]


@needs_rows
def test_a_rows_follow_the_quoted_label(parts):
    """Swap the quoted label for every other listed label that the base row offers: the answer follows (L' == human
    gold) XOR the frame's flips. decide2 is not keyed to the row's own label."""
    rows, _, ag = parts["train"]
    n = 0
    for r in rows:
        info = ag["infos"][r["rid"]]
        if info["kind"] != "a":
            continue
        base = v.golden_row(r["meta"]["derived_from"])
        labels = list(v.card_parts(v.card_of(r))["extra"])
        for L2 in labels:
            if L2 == info["L"] or L2 not in base["options"] or '"' in L2:
                continue
            q = r["instructions"].replace(f'"{info["L"]}" is the listed', f'"{L2}" is the listed')
            assert q != r["instructions"]
            want = (L2 == base["gold"]) != (info["flips"] % 2 == 1)
            assert v.decide2_row({**r, "instructions": q}) == ("yes" if want else "no"), (r["rid"], L2)
            n += 1
    assert n > 500


@needs_rows
def test_f1_outcome_rows_follow_the_named_outcome(parts):
    """A true 'the outcome ... is "x"' becomes false when x is replaced by another outcome of the same document."""
    rows, _, ag = parts["train"]
    outs = defaultdict(set)
    for r in rows:
        info = ag["infos"][r["rid"]]
        if info["kind"] == "f1.outcome":
            m = re.fullmatch(r'(the outcome of this .+? is )"([^"]+)"', info["P"])
            outs[m.group(1)].add(m.group(2))
    n = 0
    for r in rows:
        info = ag["infos"][r["rid"]]
        if info["kind"] != "f1.outcome" or not info["truth"]:
            continue
        m = re.fullmatch(r'(the outcome of this .+? is )"([^"]+)"', info["P"])
        for x2 in sorted(outs[m.group(1)] - {m.group(2)})[:2]:
            q = r["instructions"].replace(info["P"], f'{m.group(1)}"{x2}"')
            want = "no" if info["answer"] == "yes" else "yes"
            assert v.decide2_row({**r, "instructions": q}) == want, (r["rid"], x2)
            n += 1
    assert n >= 20


@needs_rows
def test_hidden_card_makes_card_dependent_rows_undefined(parts):
    rows, _, ag = parts["train"]
    seen = set()
    for r in rows:
        kind = ag["infos"][r["rid"]]["kind"]
        fam = "a" if kind == "a" else kind.split(".")[0]
        if fam in seen or r["meta"]["card_style"] == "none":
            continue
        seen.add(fam)
        hidden = {**r, "meta": {**r["meta"], "card_style": "none"}}
        got = v.decide2_row(hidden)
        if fam in ("a", "f1b", "f6"):
            assert got is v.UNDEFINED, (r["rid"], fam)
        else:
            assert got == ag["answers"][r["rid"]], (r["rid"], fam)
    assert {"a", "f1", "f1b", "f2", "f3", "f6"} <= seen


@needs_rows
def test_a_row_with_a_changed_state_is_undefined(parts):
    rows, _, ag = parts["train"]
    r = next(x for x in rows if ag["infos"][x["rid"]]["kind"] == "a")
    assert v.decide2_row({**r, "state": r["state"] + " "}) is v.UNDEFINED


@needs_rows
def test_write_agreement_goes_to_the_given_path_and_the_redirected_manifest(tmp_path, _tmp_manifest):
    out = tmp_path / "agree.json"
    rep = v.write_agreement(out)
    assert out.exists() and json.loads(out.read_text())["parts"]["train"]["agree"] == 1500
    rec = [json.loads(x) for x in _tmp_manifest.read_text().splitlines()]
    assert rec[-1]["part"] == "decide2_agreement" and rec[-1]["agree"] == {"train": [1500, 1500], "dev": [300, 300]}
    assert rep["parts"]["dev"]["disagree"] == 0
