"""Tests of yn2b/f7_precheck.py (the F7 ship audit). Tiny synthetic fixtures; each test proves a check can FAIL (and,
where a tiny fixture can satisfy it, that it PASSes on the clean fixture). CPU only; files are written to tmp_path only.
The reference-set decontamination is exercised with monkeypatched, tiny reference sets (no 1.2 GB pass in tests).

  cd opendecide-data/lean && PYTHONDONTWRITEBYTECODE=1 ../.venv/bin/python -m pytest -q -p no:cacheprovider \
      yn2b/tests/test_f7_precheck.py
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

YN2B = Path(__file__).resolve().parents[1]
LEAN = YN2B.parent
for p in (str(YN2B), str(LEAN), str(LEAN / "extra")):
    if p not in sys.path:
        sys.path.insert(0, p)
sys.dont_write_bytecode = True

import f7_precheck as f  # noqa: E402


# ================================================================================================= fixture builders
def cue(lex, cls, pos, scoping, dist="same_clause", surface=None):
    c = {"lexeme": lex, "cls": cls, "position": pos, "scoping": scoping, "distance": dist}
    if surface:
        c["surface"] = surface
    return c


def atom(v):
    return {"op": "ATOM", "id": "p", "val": bool(v)}


def core(x):
    return {"op": "CORE", "child": x}


def NOT(c, x):
    return {"op": "NOT", "cue": c, "child": x}


def DIST(c, x, **kw):
    d = {"op": "DIST", "cue": c, "child": x}
    d.update(kw)
    return d


def yn_card(q):
    st = q.rstrip("?")
    return f"- yes: {st}\n- no: it is not so that {st}"


RUNG_SPECS = {
    # rung: (instruction template, cues, lf builder(truth), gold(truth), phen)
    "R0": ("Does the text show that the post {cl} {x}?", [],
           lambda t: core(atom(t)), lambda t: t, [1]),
    "N1": ("Is it false that the post {cl} {x}?",
           [cue("false", "truth_frame", "outer_frame", True, "same_sentence")],
           lambda t: NOT(0, core(atom(t))), lambda t: not t, [3]),
    "N2": ("Is it false that the post does not {cl0} {x}?",
           [cue("false", "truth_frame", "outer_frame", True, "same_sentence"),
            cue("not", "syntactic", "inner_claim", True)],
           lambda t: NOT(0, NOT(1, core(atom(t)))), lambda t: t, [6]),
    "D": ("Whether or not the tone is calm, does the text show that the post {cl} {x}?",
          [cue("not", "syntactic", "outer_frame", False, "same_sentence")],
          lambda t: DIST(0, core(atom(t))), lambda t: t, [15]),
}


def ladder(i, truth, part="train", dev_kind="train", kind="card", source="src_a", family="fam_a", state=None,
           rungs=("R0", "N1", "N2", "D"), card_style="defs", x="spam"):
    """One ladder (call_id) of yes/no rows on one state; returns rows, metas, relations."""
    lid = f"L{part}{i}"
    st = state if state is not None else f"State text number {i} about a parcel that arrived on day {i} of the month."
    rows, metas, ids = [], [], {}
    for rg in rungs:
        tpl, cues, lfb, gb, phen = RUNG_SPECS[rg]
        q = tpl.format(cl="mentions", cl0="mention", x=x)
        gold = int(bool(gb(truth)))
        rid = f"r_{lid}_{rg}"
        rows.append({"id": rid, "group_id": f"g:{lid}", "call_id": f"c_{lid}", "split": "train" if part == "train"
                     else "probe", "track": "GD", "source": "gd_gen3_nested_negation", "state": st, "qtype": "noul",
                     "instructions": q, "options": None, "gold": gold, "card": yn_card(q), "role": "aff", "meta": {}})
        lf = lfb(truth)
        I = f.lf_analyse(lf, len(cues), False)
        metas.append({"id": rid, "ladder_id": lid, "rung": rg, "lf": lf, "truth_P": bool(truth), "depth": I.depth,
                      "n_cues": len(cues), "n_distractor": sum(1 for c in cues if not c["scoping"]),
                      "cues": copy.deepcopy(cues), "phen": list(phen), "frame_family": family, "frame_id": f"{family}_{rg}",
                      "ladder_kind": kind, "source": source, "dev_kind": dev_kind, "card_style": card_style,
                      "gold": gold})
        ids[rg] = rid
    rels = []
    if "R0" in ids and "N1" in ids:
        rels.append({"type": "complement", "a": ids["R0"], "b": ids["N1"]})
    if "R0" in ids and "N2" in ids:
        rels.append({"type": "equiv", "a": ids["R0"], "b": ids["N2"]})
    if "R0" in ids and "D" in ids:
        rels.append({"type": "inv", "a": ids["R0"], "b": ids["D"]})
    return rows, metas, rels


def dataset(n_train=8, n_dev=4, **kw):
    parts = {"train": [], "probe": [], "devx": []}
    metas, rels = [], {"train": [], "probe": [], "devx": []}
    for i in range(n_train):
        r, m, rl = ladder(i, i % 2 == 0, **kw)
        parts["train"] += r
        metas += m
        rels["train"] += rl
    for i in range(n_dev):
        r, m, rl = ladder(100 + i, i % 2 == 0, part="probe", dev_kind="iid" if i % 2 else "holdout", **kw)
        parts["probe"] += r
        metas += m
        rels["probe"] += rl
    return parts, metas, rels


def mkctx(parts=None, metas=None, rels=None, **opts):
    if parts is None:
        parts, metas, rels = dataset()
    o = f.Opts(fast=True, unseen=False, **opts)
    return f.Ctx(parts, metas, rels, o, log=lambda s: None)


def st(subs, sid):
    hit = [s for s in subs if s.id == sid]
    assert hit, f"no sub-check {sid} in {[s.id for s in subs]}"
    return hit[0].status


def meta_of(metas, rid):
    return [m for m in metas if m["id"] == rid][0]


def row_of(parts, rid):
    return [r for rows in parts.values() for r in rows if r["id"] == rid][0]


# ================================================================================================= LF evaluator
def test_lf_analyse_depth_truth_gold():
    lf = NOT(0, NOT(1, core(atom(True))))
    I = f.lf_analyse(lf, 2, False)
    assert not I.errors and I.depth == 2 and I.truth_P is True and I.gold == 1
    lf = NOT(0, DIST(1, NOT(None, core(atom(False)))))
    I = f.lf_analyse(lf, 2, False)
    assert not I.errors and I.depth == 2 and I.gold == 0 and I.has_null_not
    q = {"op": "ATLEAST", "k": 2, "children": [atom(True), atom(False), atom(True)]}
    I = f.lf_analyse(NOT(0, core(q)), 1, False)
    assert I.gold == 0 and I.truth_P is True


def test_lf_analyse_errors():
    assert f.lf_analyse({"op": "AND", "children": [core(atom(1)), core(atom(0))]}, 0, False).errors   # two COREs
    assert f.lf_analyse(core(NOT(0, atom(True))), 1, False).errors                                  # cue inside CORE
    assert f.lf_analyse(NOT(5, core(atom(True))), 1, False).errors                                  # cue out of range
    assert f.lf_analyse({"op": "XOR", "child": core(atom(1))}, 0, False).errors                      # unknown op
    ch = {"op": "CHOICE", "select": "true", "options": [core(atom(True)), core(atom(True))]}
    assert any("exactly one" in e for e in f.lf_analyse(ch, 0, True).errors)                         # two golds


def test_share_ok_integer_rule():
    assert f.share_ok(50, 100, 0.48, 0.52) and not f.share_ok(55, 100, 0.48, 0.52)
    assert f.share_ok(2, 2, 0.45, 0.55)          # within one row of an even split
    assert not f.share_ok(3, 3, 0.45, 0.55)


# ================================================================================================= check 1
def test_schema_clean_passes():
    subs = f.check_schema(mkctx())
    for sid in ("1.1", "1.2", "1.3", "1.4", "1.5", "1.6", "1.7"):
        assert st(subs, sid) == "PASS", sid


def test_schema_join_fails():
    parts, metas, rels = dataset()
    metas.append(dict(metas[0], id="orphan"))
    metas = [m for m in metas if m["id"] != parts["train"][1]["id"]]
    assert st(f.check_schema(mkctx(parts, metas, rels)), "1.1") == "FAIL"


def test_schema_missing_field_fails():
    parts, metas, rels = dataset()
    del metas[0]["frame_id"]
    assert st(f.check_schema(mkctx(parts, metas, rels)), "1.2") == "FAIL"


def test_schema_bad_lf_fails():
    parts, metas, rels = dataset()
    metas[0]["lf"] = {"op": "AND", "children": [core(atom(1)), core(atom(1))]}
    assert st(f.check_schema(mkctx(parts, metas, rels)), "1.3") == "FAIL"


def test_schema_consistency_fails():
    parts, metas, rels = dataset()
    metas[1]["depth"] = 3            # N1 really has depth 1
    assert st(f.check_schema(mkctx(parts, metas, rels)), "1.4") == "FAIL"
    parts, metas, rels = dataset()
    metas[1]["cues"][0]["scoping"] = False   # a NOT on the CORE path tagged non-scoping
    assert st(f.check_schema(mkctx(parts, metas, rels)), "1.4") == "FAIL"


def test_schema_dev_kind_fails():
    parts, metas, rels = dataset()
    meta_of(metas, parts["probe"][0]["id"])["dev_kind"] = "train"
    assert st(f.check_schema(mkctx(parts, metas, rels)), "1.5") == "FAIL"


def test_schema_row_format_and_check_rows_fail():
    parts, metas, rels = dataset()
    parts["train"][0]["options"] = ["yes", "no"]
    parts["train"][1]["gold"] = 2
    meta_of(metas, parts["train"][1]["id"])["gold"] = 2
    subs = f.check_schema(mkctx(parts, metas, rels))
    assert st(subs, "1.6") == "FAIL" and st(subs, "1.7") == "FAIL"


# ================================================================================================= check 2
def test_gold_lf_mismatch_fails():
    parts, metas, rels = dataset()
    parts["train"][0]["gold"] = 1 - parts["train"][0]["gold"]
    metas[0]["gold"] = parts["train"][0]["gold"]
    assert st(f.check_gold(mkctx(parts, metas, rels)), "2.1") == "FAIL"
    assert st(f.check_gold(mkctx()), "2.1") == "PASS"


def test_distractor_deletion_fails_on_false_presupposition():
    parts, metas, rels = dataset()
    d = [m for m in metas if m["rung"] == "D"][0]
    d["lf"]["mode"] = "presupposed"
    d["lf"]["side"] = {"op": "ATOM", "id": "s", "val": False}
    subs = f.check_gold(mkctx(parts, metas, rels))
    assert st(subs, "2.2") == "FAIL" and st(subs, "2.5") == "FAIL"
    assert st(f.check_gold(mkctx()), "2.2") == "PASS"


def test_decide2_agreement_and_independence():
    ctx = mkctx()
    assert st(f.check_gold(ctx), "2.3") == "PENDING"
    preds = {R["row"]["id"]: R["row"]["gold"] for R in ctx.R}
    preds[ctx.R[0]["row"]["id"]] = 1 - preds[ctx.R[0]["row"]["id"]]
    subs = f.check_gold(mkctx(decide2_preds=preds, decide2_independent="yes"))
    assert st(subs, "2.3") == "FAIL" and st(subs, "2.3b") == "PASS"
    assert st(f.check_gold(mkctx(decide2_preds=preds, decide2_independent="no")), "2.3b") == "FAIL"


def test_decide2_importing_generator_fails(tmp_path):
    code = tmp_path / "d2.py"
    code.write_text("import gen3_nested_negation\n")
    ctx = mkctx(decide2_preds={}, decide2_code=[str(code)], decide2_independent="yes",
                generator_code=["golden_src/gen3/gen3_nested_negation.py"])
    assert st(f.check_gold(ctx), "2.3b") == "FAIL"


def test_bivalence_line():
    parts, metas, rels = dataset()
    r = parts["train"][1]
    r["instructions"] = "Does the text refute the claim that the post mentions spam?"
    r["card"] = yn_card(r["instructions"])
    assert st(f.check_gold(mkctx(parts, metas, rels)), "2.4") == "FAIL"
    r["card"] += "\n- note: the text settles every claim asked about here"
    assert st(f.check_gold(mkctx(parts, metas, rels)), "2.4") == "PASS"


def test_presupposing_distractor_wording_fails():
    parts, metas, rels = dataset()
    d = [r for r in parts["train"] if r["id"].endswith("_D")][0]
    d["instructions"] = "Given that the post was not sent by Kim, does the text show that the post mentions spam?"
    assert st(f.check_gold(mkctx(parts, metas, rels)), "2.5") == "FAIL"


def choice_ladder(i, gold_idx=0, select="true", n_opt=3, part="train", dev_kind="train"):
    lid = f"LC{part}{i}"
    opts = [f"option {k} for {i}" for k in range(n_opt)]
    olfs = [core(atom((k == gold_idx) == (select == "true"))) for k in range(n_opt)]
    cues = [cue("false", "truth_frame", "outer_frame", True, "same_sentence")] if select == "false" else []
    lf = {"op": "CHOICE", "select": select, "options": olfs}
    if select == "false":
        lf["cue"] = 0
    rid = f"r_{lid}"
    row = {"id": rid, "group_id": f"g:{lid}", "call_id": f"c_{lid}", "split": "train", "track": "GD",
           "source": "gd_gen3_nested_negation", "state": f"choice state {i}", "qtype": "choice",
           "instructions": "Which statement is false?" if select == "false" else "Which statement is true?",
           "options": opts, "gold": opts[gold_idx], "card": None, "role": "choice", "meta": {}}
    I = f.lf_analyse(lf, len(cues), True)
    meta = {"id": rid, "ladder_id": lid, "rung": "CH", "lf": lf, "truth_P": bool(I.truth_P), "depth": I.depth,
            "n_cues": len(cues), "n_distractor": 0, "cues": cues, "phen": [37] + ([36] if select == "false" else []),
            "frame_family": "fam_c", "frame_id": "fc", "ladder_kind": "card", "source": "src_a", "dev_kind": dev_kind,
            "card_style": "none", "gold": gold_idx}
    return row, meta


def test_choice_lf_gold_fails():
    parts, metas, rels = dataset()
    row, meta = choice_ladder(0, gold_idx=1)
    meta["lf"]["options"][1], meta["lf"]["options"][0] = meta["lf"]["options"][0], meta["lf"]["options"][1]
    parts["train"].append(row)
    metas.append(meta)
    assert st(f.check_gold(mkctx(parts, metas, rels)), "2.6") == "FAIL"


# ================================================================================================= check 3
def test_coverage_floors_fail_and_pass(monkeypatch):
    assert st(f.check_coverage(mkctx()), "3.1") == "FAIL"
    monkeypatch.setitem(f.FLOORS, "full", {"MUST": (0, 0, 0), "SHOULD": (0, 0, 0), "NICE": (0, 0, 0)})
    assert st(f.check_coverage(mkctx()), "3.1") == "PASS"


def test_coverage_caps_fail():
    parts, metas, rels = dataset()
    for m in metas:
        m["phen"].append(14)
    assert st(f.check_coverage(mkctx(parts, metas, rels)), "3.2") == "FAIL"


def test_tag_consistency_fails():
    parts, metas, rels = dataset()
    metas[2]["phen"].append(9)        # N2 row (depth 2) tagged as depth 4
    assert st(f.check_coverage(mkctx(parts, metas, rels)), "3.3") == "FAIL"
    assert st(f.check_coverage(mkctx()), "3.3") == "PASS"


def test_cells_lexicon_frames_size_mix_dev_kinds_fail(monkeypatch):
    subs = f.check_coverage(mkctx())
    for sid in ("3.4", "3.5", "3.6", "3.7", "3.8", "3.9", "3.10", "3.11", "3.12"):
        assert st(subs, sid) == "FAIL", sid
    assert st(subs, "3.5b") == "PENDING"
    monkeypatch.setattr(f, "TRAIN_LADDERS_MIN", 1)
    monkeypatch.setattr(f, "TRAIN_ROWS_RESEARCH_MIN", 1)
    assert st(f.check_coverage(mkctx()), "3.7") == "PASS"


def test_lexicon_file_mismatch_fails():
    ctx = mkctx(lexicon={"lexemes": {"false": {"cls": "truth_frame"}}})
    assert st(f.check_coverage(ctx), "3.5b") == "FAIL"     # 'not' is not in the lexicon file
    ctx = mkctx(lexicon={"lexemes": {"false": {"cls": "truth_frame"}, "not": {"cls": "syntactic"}}})
    assert st(f.check_coverage(ctx), "3.5b") == "PASS"


# ================================================================================================= check 4
def test_balance_clean_cells_pass_and_skew_fails():
    subs = f.check_balance(mkctx(*dataset(n_train=40, n_dev=20)))
    assert st(subs, "4.1a") == "PASS" and st(subs, "4.3") == "PASS"
    parts, metas, rels = dataset(n_train=40, n_dev=20)
    for r in parts["train"]:            # every ladder true: the cells and truth(P) are no longer balanced
        m = meta_of(metas, r["id"])
        if not m["truth_P"]:
            m["truth_P"] = True
            m["lf"] = json.loads(json.dumps(m["lf"]).replace('"val": false', '"val": true'))
            I = f.lf_analyse(m["lf"], len(m["cues"]), False)
            r["gold"] = m["gold"] = I.gold
    subs = f.check_balance(mkctx(parts, metas, rels))
    assert st(subs, "4.1a") == "FAIL" and st(subs, "4.3") == "FAIL"


def test_balance_stratum_fails():
    parts, metas, rels = dataset(n_train=40, n_dev=20)
    for r in parts["train"]:
        if r["gold"] == 1:
            meta_of(metas, r["id"])["frame_id"] = "always_yes_frame"
    assert st(f.check_balance(mkctx(parts, metas, rels)), "4.2a") == "FAIL"


def test_truth_per_label_fails():
    parts, metas, rels = dataset(n_train=40, n_dev=20)
    for r in parts["train"]:
        m = meta_of(metas, r["id"])
        m["quoted_label"] = "spam" if m["truth_P"] else "ham"
    assert st(f.check_balance(mkctx(parts, metas, rels)), "4.4") == "FAIL"


def test_choice_rows_required_and_positions(monkeypatch):
    assert st(f.check_balance(mkctx()), "4.5") == "FAIL"     # no choice rows
    parts, metas, rels = dataset(n_train=8, n_dev=4)
    for i in range(3):                                         # 3 choice rows / 35 rows, all gold at position 0
        row, meta = choice_ladder(i, gold_idx=0)
        parts["train"].append(row)
        metas.append(meta)
    assert st(f.check_balance(mkctx(parts, metas, rels)), "4.5") == "FAIL"


def test_cardless_rule_fails():
    parts, metas, rels = dataset(n_train=40, n_dev=20)
    parts["train"][0]["card"] = None                           # an R0 row without a card, not 'Is it true that'
    assert st(f.check_balance(mkctx(parts, metas, rels)), "4.6") == "FAIL"


def test_card_style_per_depth_fails():
    parts, metas, rels = dataset(n_train=40, n_dev=20)
    for m in metas:
        if m["depth"] == 2:
            m["card_style"] = "lower"
    assert st(f.check_balance(mkctx(parts, metas, rels)), "4.6b") == "FAIL"


def test_distractor_parity_ar_cue_mix_lexeme_position_rules_fail():
    parts, metas, rels = dataset(rungs=("R0", "N1", "N2"))
    subs = f.check_balance(mkctx(parts, metas, rels))
    for sid in ("4.7", "4.8", "4.9", "4.10", "4.11", "4.14"):
        assert st(subs, sid) == "FAIL", sid


def test_lexeme_parity_fails():
    parts, metas, rels = dataset(rungs=("R0", "N1"))          # 'false' only ever in odd-depth rows
    assert st(f.check_balance(mkctx(parts, metas, rels)), "4.12") == "FAIL"


def test_distractor_capable_lexeme_fails():
    parts, metas, rels = dataset(rungs=("R0", "N1", "N2"))    # 'not' (syntactic) is never used as a distractor
    assert st(f.check_balance(mkctx(parts, metas, rels)), "4.13") == "FAIL"
    assert st(f.check_balance(mkctx()), "4.13") == "PASS"


def test_state_negation_balance_fails():
    parts, metas, rels = dataset(n_train=40, n_dev=20)
    for r in parts["train"] + parts["probe"]:
        if meta_of(metas, r["id"])["truth_P"]:
            r["state"] = r["state"] + " The parcel did not arrive on time."
    assert st(f.check_balance(mkctx(parts, metas, rels)), "4.15") == "FAIL"


# ================================================================================================= check 5
def test_surface_probes_detect_leaks():
    subs = f.check_probes(mkctx())
    assert st(subs, "5.a1") == "PASS"
    parts, metas, rels = dataset(n_train=20, n_dev=8)
    for r in parts["train"] + parts["probe"]:
        if r["gold"] == 0:
            r["instructions"] = r["instructions"].rstrip("?") + " or not?"
    subs = f.check_probes(mkctx(parts, metas, rels))
    assert st(subs, "5.c") == "FAIL"
    assert st(subs, "5.j") == "FAIL"                        # no choice rows at all


def test_frame_majority_probe_fails():
    parts, metas, rels = dataset(n_train=20, n_dev=8)
    for m in metas:
        m["frame_id"] = "F_yes" if m["gold"] == 1 else "F_no"
    assert st(f.check_probes(mkctx(parts, metas, rels)), "5.g1") == "FAIL"


def test_bow_probe_fails_on_leaky_word():
    parts, metas, rels = dataset(n_train=20, n_dev=8)
    for r in parts["train"] + parts["probe"]:
        r["instructions"] += " Kindly." if r["gold"] else " Briefly."
    subs = f.check_probes(f.Ctx(parts, metas, rels, f.Opts(fast=False, unseen=False), log=lambda s: None))
    assert st(subs, "5.h") == "FAIL"


def test_correlation_fails():
    parts, metas, rels = dataset(n_train=20, n_dev=8)
    for r in parts["train"] + parts["probe"]:
        meta_of(metas, r["id"])["card_style"] = "upper" if r["gold"] else "defs"
    assert st(f.check_probes(mkctx(parts, metas, rels)), "5.k") == "FAIL"


def test_yes_line_restatement_fails():
    parts, metas, rels = dataset()
    r = parts["train"][1]                                        # N1 'Is it false that ...'
    r["card"] = "- yes: the post mentions spam\n- no: the post does not mention spam"
    assert st(f.check_probes(mkctx(parts, metas, rels)), "5.l") == "FAIL"
    assert st(f.check_probes(mkctx()), "5.l") == "PASS"


# ================================================================================================= check 6
def test_composition_c1_c2_fail_without_negation_mix():
    parts, metas, rels = dataset(rungs=("R0",))                 # gold = truth(P) everywhere
    subs = f.check_composition(mkctx(parts, metas, rels))
    assert st(subs, "6.C1a") == "FAIL" and st(subs, "6.C2a") == "FAIL"
    assert st(subs, "6.C7a") == "FAIL"                          # no item-21 rows


def test_composition_c7_and_cue_share(monkeypatch):
    parts, metas, rels = dataset(n_train=10)
    for m in metas:
        if m["rung"] == "N1":
            m["phen"].append(21)
            m["antonym_gold"] = m["gold"]                       # the antonym reading is never wrong
    subs = f.check_composition(mkctx(parts, metas, rels))
    assert st(subs, "6.C7a") == "FAIL"
    monkeypatch.setattr(f, "CUE_SHARE_MIN_ROWS", 1)
    parts, metas, rels = dataset(rungs=("R0", "N1"))
    assert st(f.check_composition(mkctx(parts, metas, rels)), "6.CSa") == "FAIL"


# ================================================================================================= check 7
@pytest.mark.parametrize("x,text", [
    ("X1", "Doesn't the message ask for a refund?"),
    ("X2", "Is the reviewer not unhappy?"),
    ("X3", "The food was not good, it was superb."),
    ("X4", "The agent may not close the ticket."),
    ("X5", "All the messages don't mention a refund."),
    ("X6", "The caller doesn't think the charge is valid."),
    ("X7", "The agent did not notice that the card had expired."),
    ("X8", "I didn't get no refund."),
    ("X9", "The bank did not refund me on Monday."),
    ("X10", "Is it true that not all reviews praise it?"),
    ("X11", "No wonder the card was declined."),
    ("X12", "Is it true that the message mentions any refund. Yes."),
])
def test_exclude_regexes_hit(x, text):
    parts, metas, rels = dataset()
    parts["train"][0]["instructions"] = text
    ctx = mkctx(parts, metas, rels)
    h = f.exclude_hits(ctx, ctx.by_rowid[parts["train"][0]["id"]])
    assert x in h, (x, dict(h))


def test_exclude_clean_and_state_exempt():
    parts, metas, rels = dataset()
    for r in parts["train"] + parts["probe"]:
        r["state"] += " I didn't get no refund and the agent may not call."
    subs = f.check_exclude(mkctx(parts, metas, rels))
    assert st(subs, "7.1") == "PASS"
    assert subs[0].detail["state_hits_tagged_not_counted"]


def test_exclude_meta_stacks_fail():
    parts, metas, rels = dataset()
    m = metas[2]
    m["cues"].append(cue("un-", "affixal", "inner_claim", False))
    m["cues"].append(cue("never", "syntactic", "inner_claim", False))
    m["n_cues"] = len(m["cues"])
    m["lf"] = DIST(2, DIST(3, m["lf"]))
    m["n_distractor"] = 2
    ctx = mkctx(parts, metas, rels)
    assert "X12" in f.exclude_hits(ctx, ctx.by_rowid[m["id"]])


def test_inner_negative_question_needs_yes_no_lines():
    parts, metas, rels = dataset()
    r = parts["train"][0]
    r["instructions"] = "Does the post not mention spam?"
    r["card"] = "- spam: unwanted mail"
    ctx = mkctx(parts, metas, rels)
    assert "X1" in f.exclude_hits(ctx, ctx.by_rowid[r["id"]])
    r["card"] = "- yes: the post does not mention spam\n- no: the post mentions spam"
    ctx = mkctx(parts, metas, rels)
    assert "X1" not in f.exclude_hits(ctx, ctx.by_rowid[r["id"]])


# ================================================================================================= check 8
def test_decontam_cheap_checks_fail():
    parts, metas, rels = dataset()
    parts["train"][0]["instructions"] = "Is it correct that the post mentions spam?"
    meta_of(metas, parts["train"][1]["id"])["source"] = "banking77"
    subs = f.check_decontam(mkctx(parts, metas, rels))
    assert st(subs, "8.7") == "FAIL" and st(subs, "8.15") == "FAIL" and st(subs, "8.14") == "FAIL"
    assert st(subs, "8.13") == "PENDING"


def test_spec_cue_share_fails():
    parts, metas, rels = dataset(n_train=40, n_dev=0, rungs=("R0", "N1"))   # 'false' rows are all odd
    assert st(f.check_decontam(mkctx(parts, metas, rels)), "8.9") == "FAIL"


def test_ohs3_frames_read_from_code_text():
    frames = f.ohs3_frames()
    assert len(frames) == 6 and all("{p}" in x for x in frames)


def test_failure_frame_runs_loaded():
    runs, n = f.failure_frame_runs()
    assert n > 0 and runs


def test_decontam_full_with_tiny_refs(monkeypatch, tmp_path):
    import build_fix1 as bf
    import check_yn2b as cy
    parts, metas, rels = dataset()
    leak_state = "this exact sentence comes from a held out evaluation file and must never be used in training rows"
    parts["train"][0]["state"] = leak_state                       # 12-gram contact (8.1)
    for r in parts["train"][:4]:
        r["state"] = leak_state                                   # keep the ladder state identical
    parts["train"][4]["instructions"] = "Would it be an error to maintain that the post mentions spam?"  # OHS-3 T1
    parts["train"][8]["instructions"] = ("Should the statement that the tweet does not contain only non-hateful "
                                         "content be rejected?")                                   # failure frame
    parts["train"][12]["instructions"] = "Is the following sentence true or false? The post mentions spam."
    refs = {"strict": set(cy.ghash(leak_state)), "infam": set(), "infam_y": set(), "t6_dev": set(), "t6_v11": set(),
            "ids": {parts["train"][16]["id"]}, "pairs": set(), "g12": {}, "ydev_states": set(),
            "template_sets": {}}
    monkeypatch.setattr(bf, "load_refs", lambda log: refs)
    gt = tmp_path / "golden.jsonl"
    gt.write_text(json.dumps({"id": "g1", "state": parts["train"][20]["state"],
                              "instructions": parts["train"][20]["instructions"], "card": None}) + "\n")
    man = tmp_path / "neg.json"
    man.write_text(json.dumps({"sources": [{"name": "recalled", "path": str(YN2B / "decontam_only" /
                                                                             "recalled_negation_templates.json"),
                                            "format": "template_list", "fields": ["templates"]}]}))
    monkeypatch.setattr(f, "heldout_name_hits", lambda names: [])
    ctx = mkctx(parts, metas, rels, golden_train=str(gt), neg_manifest=str(man))
    ctx.opts.fast = False
    subs = f.decontam_full(ctx, __import__("collections").defaultdict(set), [])
    assert st(subs, "8.1") == "FAIL"
    assert st(subs, "8.4") == "FAIL"
    assert st(subs, "8.5") == "FAIL"
    assert st(subs, "8.6") == "FAIL"
    assert st(subs, "8.8") == "FAIL"
    assert st(subs, "8.11") == "FAIL"


def test_names_pool_split_fails(monkeypatch):
    sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
    import mv_core as mv
    pools = mv._pools()
    dev_name = f"{pools['dev_holdout']['first'][0]} {pools['dev_holdout']['last'][0]}"
    parts, metas, rels = dataset(kind="record")
    for r in parts["train"][:4]:
        r["state"] = f"Submitted by: {dev_name}\nitem list"
    monkeypatch.setattr(f, "heldout_name_hits", lambda names: [])
    s = f.names_check(mkctx(parts, metas, rels))
    assert s.status == "FAIL" and s.value["wrong_pool"] > 0
    monkeypatch.setattr(f, "heldout_name_hits", lambda names: list(names)[:1])
    parts, metas, rels = dataset(kind="record")
    tr = f"{pools['train']['first'][0]} {pools['train']['last'][0]}"
    for r in parts["train"][:4]:
        r["state"] = f"Submitted by: {tr}\nitem list"
    assert f.names_check(mkctx(parts, metas, rels)).status == "FAIL"


def test_neg_bench_manifest_missing_source_fails(tmp_path):
    man = tmp_path / "neg.json"
    man.write_text(json.dumps({"sources": [{"name": "nothing", "path": str(tmp_path / "none*.csv"), "format": "csv",
                                            "fields": ["x"]}]}))
    runs, info = f.load_neg_bench(str(man), lambda s: None)
    assert info["missing"] == ["nothing"]


# ================================================================================================= check 9
def test_ladders_clean_pass():
    subs = f.check_ladders(mkctx())
    for sid in ("9.1", "9.2", "9.3", "9.5", "9.6", "9.7"):
        assert st(subs, sid) == "PASS", sid


def test_ladder_state_size_fail():
    parts, metas, rels = dataset()
    parts["train"][1]["state"] = "a different state"
    assert st(f.check_ladders(mkctx(parts, metas, rels)), "9.1") == "FAIL"
    parts, metas, rels = dataset()
    for k in range(2):
        r = copy.deepcopy(parts["train"][0])
        r["id"] += f"_x{k}"
        parts["train"].append(r)
        m = copy.deepcopy(metas[0])
        m["id"] = r["id"]
        metas.append(m)
    assert st(f.check_ladders(mkctx(parts, metas, rels)), "9.2") == "FAIL"


def test_relations_parity_fail():
    parts, metas, rels = dataset()
    rels["train"][1]["type"] = "complement"            # R0 <-> N2 are the same parity
    assert st(f.check_ladders(mkctx(parts, metas, rels)), "9.3") == "FAIL"


def test_r0_both_golds_rungs_split_fail():
    parts, metas, rels = dataset(rungs=("N1", "N2"))
    assert st(f.check_ladders(mkctx(parts, metas, rels)), "9.4") == "FAIL"
    parts, metas, rels = dataset(rungs=("R0", "N2", "D"))   # all rows share one gold
    assert st(f.check_ladders(mkctx(parts, metas, rels)), "9.5") == "FAIL"
    parts, metas, rels = dataset()
    metas[2]["rung"] = "N3"
    assert st(f.check_ladders(mkctx(parts, metas, rels)), "9.6") == "FAIL"
    parts, metas, rels = dataset(rungs=("N1", "D"))         # D without its no-distractor twin
    assert st(f.check_ladders(mkctx(parts, metas, rels)), "9.6") == "FAIL"
    parts, metas, rels = dataset()
    pid = parts["probe"][0]["id"]
    meta_of(metas, pid)["ladder_id"] = metas[0]["ladder_id"]
    assert st(f.check_ladders(mkctx(parts, metas, rels)), "9.7") == "FAIL"


# ================================================================================================= check 10
def test_holdout_declared_items_leak_fail():
    spec = {"lexemes": ["false"], "frame_families": ["fam_a"], "sources": ["src_a"],
            "cue_combos": [["truth_frame"]]}
    subs = f.check_holdout(mkctx(holdout_spec=spec))
    for sid in ("10.1", "10.2", "10.3", "10.4"):
        assert st(subs, sid) == "FAIL", sid
    assert st(subs, "10.5") == "FAIL"


def test_holdout_text_leak_with_inflection():
    parts, metas, rels = dataset()
    for m in metas:
        if m["dev_kind"] == "holdout" and m["rung"] == "N1":
            m["cues"][0]["lexeme"] = "refute"
    parts["train"][0]["instructions"] = "Does the text refutes that the post mentions spam?"
    assert st(f.check_holdout(mkctx(parts, metas, rels)), "10.1") == "FAIL"


def test_holdout_state_overlap_iid_equal_group_fail():
    parts, metas, rels = dataset()
    hold = [r for r in parts["probe"] if meta_of(metas, r["id"])["dev_kind"] == "holdout"]
    iid = [r for r in parts["probe"] if meta_of(metas, r["id"])["dev_kind"] == "iid"]
    lid_h = meta_of(metas, hold[0]["id"])["ladder_id"]
    for r in hold:
        if meta_of(metas, r["id"])["ladder_id"] == lid_h:
            r["state"] = parts["train"][0]["state"]
    lid_i = meta_of(metas, iid[0]["id"])["ladder_id"]
    for r in iid:
        if meta_of(metas, r["id"])["ladder_id"] == lid_i:
            r["state"] = parts["train"][0]["state"]
            r["group_id"] = parts["train"][0]["group_id"]
    subs = f.check_holdout(mkctx(parts, metas, rels))
    assert st(subs, "10.6") == "FAIL" and st(subs, "10.7") == "FAIL"


def test_holdout_golden_state_and_plain_ladder_fail(tmp_path):
    parts, metas, rels = dataset()
    gt = tmp_path / "golden.jsonl"
    gt.write_text(json.dumps({"id": "g1", "state": parts["probe"][0]["state"], "instructions": "x"}) + "\n")
    ctx = f.Ctx(parts, metas, rels, f.Opts(fast=False, unseen=False, golden_train=str(gt)), log=lambda s: None)
    subs = f.check_holdout(ctx)
    assert st(subs, "10.8") == "FAIL"
    assert st(subs, "10.9") == "FAIL"        # the holdout ladders use only train frames, lexemes and sources


# ================================================================================================= check 11 + main
def test_blind_read():
    assert st(f.check_blind(mkctx()), "11.1") == "PENDING"
    ctx = mkctx()
    blind = [{"id": R["row"]["id"], "verdict": "ok"} for R in ctx.ok]
    blind[0]["verdict"] = "wrong_gold"
    assert st(f.check_blind(mkctx(blind=blind)), "11.1") == "FAIL"
    sample = f.blind_sample(mkctx())
    assert sample and all("gold" not in x for x in sample)


def test_main_writes_report_and_exit_code(tmp_path):
    parts, metas, rels = dataset()
    paths = {}
    for k, rows in (("train", parts["train"]), ("probe", parts["probe"])):
        p = tmp_path / f"t_{k}.jsonl"
        p.write_text("".join(json.dumps(r) + "\n" for r in rows))
        paths[k] = p
        (tmp_path / f"t_{k}_relations.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rels[k]))
    mp = tmp_path / "meta.jsonl"
    mp.write_text("".join(json.dumps(m) + "\n" for m in metas))
    out = tmp_path / "rep.json"
    code = f.main(["--train", str(paths["train"]), "--probe", str(paths["probe"]), "--devx", str(tmp_path / "none.jsonl"),
                   "--meta", str(mp), "--fast", "--no-unseen", "--out", str(out)])
    rep = json.loads(out.read_text())
    assert code == 1 and rep["verdict"] == "FAIL"
    assert set(rep["checks"]) == {str(i) for i in range(1, 12)}


# ================================================================================================= arbiter fixes (2 Oct)
def _add_choice_rows(parts, metas, n_true, n_false):
    for i in range(n_true):
        row, meta = choice_ladder(200 + i, gold_idx=i % 3, select="true")
        parts["train"].append(row)
        metas.append(meta)
    for i in range(n_false):
        row, meta = choice_ladder(300 + i, gold_idx=i % 3, select="false")
        parts["train"].append(row)
        metas.append(meta)


def test_truthp_per_depth_counts_yes_no_rows_only():
    """O1: on a choice row truth_P == (depth even) by definition, so 'per depth' is measured on yes/no rows."""
    parts, metas, rels = dataset(n_train=40, n_dev=20)
    _add_choice_rows(parts, metas, 5, 5)          # depth 0 (truth_P true) and depth 1 (truth_P false), 5 each
    ctx = mkctx(parts, metas, rels)
    for R in ctx.train:
        if not R["an"]["yn"]:
            assert bool(R["an"]["truth_P"]) == (R["an"]["depth"] % 2 == 0)
    sub = [s for s in f.check_balance(ctx) if s.id == "4.3"][0]
    assert sub.status == "PASS", sub.detail
    # the CH rung is still held to 48-52% over all choice rows: all choice rows at an even depth fails
    parts, metas, rels = dataset(n_train=40, n_dev=20)
    _add_choice_rows(parts, metas, 10, 0)
    sub = [s for s in f.check_balance(mkctx(parts, metas, rels)) if s.id == "4.3"][0]
    assert sub.status == "FAIL" and "train:rung=CH" in sub.detail


def test_lexicon_rule_binds_generator_rows_not_devx():
    """O2 / 3.5b: the curated-lexicon rule (CL:261) binds the generator, not the blind hand-written devx."""
    parts, metas, rels = dataset()
    r, m, rl = ladder(900, True, part="devx", dev_kind="devx")
    for mm in m:
        for c in mm["cues"]:
            c["lexeme"] = "omits" if c["lexeme"] == "not" else c["lexeme"]
    parts["devx"] += r
    metas += m
    lex = {"lexemes": {"false": {"cls": "truth_frame"}, "not": {"cls": "syntactic"}}}
    assert st(f.check_coverage(mkctx(parts, metas, rels, lexicon=lex)), "3.5b") == "PASS"
    meta_of(metas, parts["train"][2]["id"])["cues"][1]["lexeme"] = "omits"      # an N2 train row off the lexicon
    assert st(f.check_coverage(mkctx(parts, metas, rels, lexicon=lex)), "3.5b") == "FAIL"


def test_item26_tag_accepts_set_form_over_three_members():
    """O2 / 3.3: 'none / not all' written as NOT(OR) / NOT(AND) over >= 3 batch members is item 26."""
    parts, metas, rels = dataset(kind="multitext")
    for m in metas:
        if m["rung"] == "N1":
            t = m["truth_P"]
            m["lf"] = NOT(0, core({"op": "OR", "children": [atom(t), atom(False), atom(False)]}))
            m["phen"].append(26)
    assert st(f.check_coverage(mkctx(parts, metas, rels)), "3.3") == "PASS"
    for m in metas:
        if m["rung"] == "N1":
            m["lf"]["child"]["child"]["children"] = m["lf"]["child"]["child"]["children"][:2]   # 2 members: not 26
    assert st(f.check_coverage(mkctx(parts, metas, rels)), "3.3") == "FAIL"


def test_lexicon_cannot_remove_distractor_capability():
    """A1: can_distract=false in the audited lexicon no longer exempts a syntactic lexeme from CL:351."""
    parts, metas, rels = dataset(rungs=("R0", "N1", "N2"))    # 'not' (syntactic) never used as a distractor
    lex = {"lexemes": {"not": {"cls": "syntactic", "can_distract": False},
                       "false": {"cls": "truth_frame", "can_distract": False}}}
    sub = [s for s in f.check_balance(mkctx(parts, metas, rels, lexicon=lex)) if s.id == "4.13"][0]
    assert sub.status == "FAIL" and "not" in sub.detail and "false" not in sub.detail
    lex["lexemes"]["false"]["can_distract"] = True             # the lexicon can still ADD capability
    sub = [s for s in f.check_balance(mkctx(parts, metas, rels, lexicon=lex)) if s.id == "4.13"][0]
    assert "false" in sub.detail
    lex["lexemes"]["false"]["can_distract"] = False
    assert st(f.check_balance(mkctx(lexicon=lex)), "4.13") == "PASS"   # clean fixture: 'not' is a D-rung distractor


def test_identical_row_inside_one_ladder_fails_dedupe(monkeypatch, tmp_path):
    """A2: a row that repeats another row of the same ladder byte for byte fails 8.11."""
    import build_fix1 as bf
    parts, metas, rels = dataset()
    assert f.dup_rows_in_ladder(mkctx(parts, metas, rels)) == []
    refs = {"strict": set(), "infam": set(), "infam_y": set(), "t6_dev": set(), "t6_v11": set(), "ids": set(),
            "pairs": set(), "g12": {}, "ydev_states": set(), "template_sets": {}}
    monkeypatch.setattr(bf, "load_refs", lambda log: refs)
    monkeypatch.setattr(f, "heldout_name_hits", lambda names: [])
    gt = tmp_path / "golden.jsonl"
    gt.write_text(json.dumps({"id": "g1", "state": "unrelated golden state", "instructions": "q", "card": None}) + "\n")
    man = tmp_path / "neg.json"
    man.write_text(json.dumps({"sources": [{"name": "recalled", "path": str(YN2B / "decontam_only" /
                                                                             "recalled_negation_templates.json"),
                                            "format": "template_list", "fields": ["templates"]}]}))

    def run(parts, metas, rels):
        ctx = mkctx(parts, metas, rels, golden_train=str(gt), neg_manifest=str(man))
        ctx.opts.fast = False
        return f.decontam_full(ctx, __import__("collections").defaultdict(set), [])

    assert st(run(parts, metas, rels), "8.11") == "PASS"
    dup = copy.deepcopy(parts["train"][1])
    dup["id"] = dup["id"] + "_copy"
    parts["train"].append(dup)
    metas.append(dict(copy.deepcopy(meta_of(metas, parts["train"][1]["id"])), id=dup["id"]))
    assert f.dup_rows_in_ladder(mkctx(parts, metas, rels)) == [dup["id"]]
    assert st(run(parts, metas, rels), "8.11") == "FAIL"
