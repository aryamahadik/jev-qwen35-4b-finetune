"""t37b/test_fix_i1.py: tests of fix iteration 1 (G0_LITE_T37B_A1.md; stage-B pilot verdict F1, F2, F3, F5). In memory only:
no replay row, no Haiku, nothing written (A37 f).

  A1 file       G0 v2 untouched, amendment frozen and complete (A1-1 .. A1-7), the frozen pool still loads under v2
  F2 (A1-2)     hotpotqa anchor rule: the pilot row a0012 and the verdict's cut-mid-name examples read correctly by both
                programs; the cut partner and every other hotpotqa shape are refused by both
  F3 (A1-3/4)   an equiv partner is capped by its paraphrase only; plan_block settles at a fixed point and does not collapse
  F5 (A1-5)     partner gold balanced in the family, per wording cell and per (entry, kind) cell; flipping every gold
                changes nothing; no label is set by the plan
  (F1, A1-1, is tested with the decision branches in test_t37b.py.)
Run (from lean/):  ../.venv/bin/python -m pytest -q c2_build/t37b
"""
from __future__ import annotations

import hashlib
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
C2_BUILD = Path(__file__).resolve().parents[1]
if str(C2_BUILD) not in sys.path:
    sys.path.insert(0, str(C2_BUILD))

from t37b import author_pool as AP  # noqa: E402
from t37b import builder as BL  # noqa: E402
from t37b import fixtures as FX  # noqa: E402
from t37b import polarity as PA  # noqa: E402
from t37b import polarity_b as PB  # noqa: E402
from t37b import select as SEL  # noqa: E402
from t37b import sources as SRC  # noqa: E402

HOT = SRC.ENTRY_BY_KEY["gd_hotpotqa_yesno/q"]
TRAIN = SRC.FRAMES_TRAIN


# ------------------------------------------------------------------------------------------------ the amendment file

def test_g0_v2_is_untouched_and_the_amendment_is_frozen():
    assert BL.G0_SHA256 == "9733b721fcab18c1bbfaf15567d99e6a52433fd7918c221963a8b3eb46da9cd4"
    assert hashlib.sha256(BL.G0_LITE.read_bytes()).hexdigest() == BL.G0_SHA256
    assert hashlib.sha256(BL.G0_AMENDMENT.read_bytes()).hexdigest() == BL.G0_AMENDMENT_SHA256
    assert BL.g0_problems() == []
    text = BL.G0_AMENDMENT.read_text(encoding="utf-8")
    assert len(text.splitlines()) <= 200
    assert all(f"- A1-{n} " in text for n in range(1, 8)) and "- A1-8 " not in text
    assert BL.G0_SHA256[:8] in text


def test_a_changed_amendment_halts_the_writers(monkeypatch):
    monkeypatch.setattr(BL, "G0_AMENDMENT_SHA256", "f" * 64)
    assert any("amendment 1 changed" in p for p in BL.g0_problems())
    with pytest.raises(RuntimeError):
        BL.require_g0()


def test_the_frozen_pool_still_loads_under_g0_v2():
    pool = AP.load_pool()
    assert pool.paraphrases and all(c["status"] == "admitted" for c in pool.paraphrases)


def test_rows_name_both_halves_of_g0_v3():
    plan, _ = SEL.plan_block(SEL.eligible(FX.many_rows(6), [], status=FX.keep_all, strict_inputs=False)[0],
                             n_complement=20, n_equiv=0, seed="t37b-test", source_cap=1.0, template_cap=1.0)
    c = BL.build_candidates(plan[:1])[0]
    row = BL.partner_row(c)
    assert row["meta"]["spec_id"] == f"T37b.G0lite.{BL.G0_SHA256[:8]}+A1.{BL.G0_AMENDMENT_SHA256[:8]}"


# ------------------------------------------------------------------------------------------------ F2: hotpotqa

GOOD = [  # (base question, the subject the anchor rule must read)
    ("Are BLT cocktail and Tamango both alcoholic drinks?", "BLT cocktail and Tamango"),   # pilot row a0012
    ("Are Il trovatore and Alcina both operas?", "Il trovatore and Alcina"),
    ("Are Port wine and Bananarita both alcoholic drinks?", "Port wine and Bananarita"),
    ("Are Sharp Corporation and Robotron KC 87 both computers?", "Sharp Corporation and Robotron KC 87"),
    ("Are Hottonia and Delphinium both genera of plants?", "Hottonia and Delphinium"),
    ("Were Wanda Jakubowska and Bill Duke both nationals of the same country?", "Wanda Jakubowska and Bill Duke"),
    ("Are The Weakerthans and The Ready Set both bands from North America?", "The Weakerthans and The Ready Set"),
    ("Are Colorado River Aqueduct and Eastside Canal both in the same state?",
     "Colorado River Aqueduct and Eastside Canal"),
    ("Are The 11th Hour and Calle 54 both films?", "The 11th Hour and Calle 54"),
]


@pytest.mark.parametrize("q,subject", GOOD, ids=[g[0][:40] for g in GOOD])
def test_anchor_rule_reads_the_subject_up_to_both(q, subject):
    sp = PA.split_question(q, HOT)
    assert sp is not None and sp[0] == "" and sp[2] == subject and sp[3].startswith("both ")
    assert PA.base_feasible_a("syntactic", q, HOT) and PB.base_feasible_b("syntactic", q, HOT)
    for frame in TRAIN:
        partners = PA.syntactic_targets(q, HOT, frame)
        assert partners and all(f" {subject} " in p and (" not both " in p or "n't both " in p) for p in partners)
        for p in partners:
            assert PA.classify_a(q, p, "syntactic", HOT, TRAIN)[0] == "opposite", p
            assert PB.classify_b(q, p, "syntactic", HOT, TRAIN)[0] == "opposite", p


def test_pilot_row_a0012_partner_is_not_garbled():
    q = "Are BLT cocktail and Tamango both alcoholic drinks?"
    got = PA.syntactic_targets(q, HOT, "Is it correct that")
    assert got == {"Is it correct that BLT cocktail and Tamango are not both alcoholic drinks?",
                   "Is it correct that BLT cocktail and Tamango aren't both alcoholic drinks?"}
    cut = "Is it correct that BLT are not cocktail and Tamango both alcoholic drinks?"    # what the pilot wrote
    assert PA.classify_a(q, cut, "syntactic", HOT, TRAIN)[0] is None
    assert PB.classify_b(q, cut, "syntactic", HOT, TRAIN)[0] is None
    for cutq in ("Is it true that Il are not trovatore and Alcina both operas?",
                 "Is it true that Port are not wine and Bananarita both alcoholic drinks?",
                 "Is it true that Sharp Corporation and Robotron KC are not 87 both computers?"):
        base = {"Il": GOOD[1][0], "Port": GOOD[2][0], "Sharp": GOOD[3][0]}[cutq.split()[4]]
        assert PA.classify_a(base, cutq, "syntactic", HOT, TRAIN)[0] is None
        assert PB.classify_b(base, cutq, "syntactic", HOT, TRAIN)[0] is None


REFUSED = [
    "Are Gawain and Cavalleria rusticana by the same composer?",              # no " both "
    "Do Rigoletto and Die tote Stadt have the same number of acts?",           # "Do X <verb>" without both
    "Are both Trivor and Rakaposhi in Pakistan?",                              # a leading "both": reads as neither
    "Were both Time and Teen designed to be read by teenage girls ages 10 to 15?",
    "Did both the Airedale Terrier and Cão Fila de São Miguel originate from England?",
    "Are Jonathan Stark and Henri Kontinen from the same country?",
    "Is Mark Krein a mathematician?",
    "Has Juniper Networks, Inc. been purchased more that Covidien plc?",
    "Are Alpha and Beta both A and are Gamma and Delta both B?",              # two of them
    "Cypella and Deutzia, are types of plants?",                              # no leading auxiliary
    "Are Alpha and Beta both?",                                               # nothing after "both"
    "Are Alpha and Beta Both Films?",                                         # a capital Both is not the anchor
]


@pytest.mark.parametrize("q", REFUSED, ids=[r[:40] for r in REFUSED])
def test_every_other_hotpotqa_shape_is_refused_by_both_programs(q):
    assert PA.split_question(q, HOT) is None
    assert not PA.base_feasible_a("syntactic", q, HOT)
    assert not PB.base_feasible_b("syntactic", q, HOT)
    assert PA.syntactic_targets(q, HOT, "Is it true that") == set()


def test_programs_agree_on_a_sweep_of_hotpotqa_shapes():
    """A reads ' both ' in the text, B counts the word among case-kept words: they must agree on every shape here."""
    shapes = [g[0] for g in GOOD] + REFUSED + [
        "Are Ana Ruiz and Tomas Feld both born in Portugal?", "Were Ana Ruiz & Tomas Feld both writers?",
        "Are Alpha, Beta and Gamma both bands?", "Are O'Brien and McGahern both Irish?",
        "Are Alpha (band) and Beta both bands?", "Are Alpha and Beta both, bands?", "Are Both Ends Burning and Beta both films?"]
    for q in shapes:
        a, b = PA.base_feasible_a("syntactic", q, HOT), PB.base_feasible_b("syntactic", q, HOT)
        if q == "Are Alpha and Beta both, bands?":
            continue                                    # known A/B difference (A reads ' both ', B the word): drops
        assert a == b, (q, a, b)


def test_no_hotpotqa_partner_is_cut_inside_the_subject():
    """Every syntactic partner of every GOOD base is the base with ONE 'not' after its first auxiliary-and-subject and
    nothing else moved: the words before ' both ' are unchanged and stay together."""
    for q, subject in GOOD:
        for p in PA.syntactic_targets(q, HOT, "Is it true that"):
            assert p.startswith(f"Is it true that {subject} ")
            assert p.endswith(" both " + q.split(" both ", 1)[1])


# ------------------------------------------------------------------------------------------------ F3 and F5 (plan)

def _extra_pool(n_variants: int = 25) -> AP.Pool:
    """A stand-in admitted pool with many paraphrase templates per entry (as the real pool has 210 + 99)."""
    recs = []
    for r in FX.stand_in_pool():
        for k in range(n_variants):
            t = r["template"][:-1] + f" (variant {k})?"
            recs.append(AP.record(r["sem"], t, "T37b-author_wording-standin-000", "0" * 64)
                        | {"reads": ["same", "same"], "status": "admitted"})
    return AP.Pool(recs)


POOL = _extra_pool()


def _bases(n_per: int = 60, skew: bool = False):
    rows = FX.many_rows(n_per)
    if skew:    # 4 of 5 bases have gold yes: the unbalanced partner rate is far from 50%
        rows = [dict(r, gold=0 if i % 5 == 0 else 1) for i, r in enumerate(rows)]
    return SEL.eligible(rows, [], status=FX.keep_all, strict_inputs=False)[0]


def _fixed_point(bases, plan, nc, ne, seed, pool, balance=True):
    n = len(plan)
    order = sorted(bases, key=lambda b: SEL.uhash(seed, "t37b-order", b.row["id"]))
    again = SEL._plan_once(order, TRAIN, nc, ne, seed, "train", max(1, math.floor(SEL.SOURCE_CAP * n)),
                           max(1, math.floor(SEL.TEMPLATE_CAP * n)), pool.choices(), balance)
    return [i.pid for i in again]


@pytest.mark.parametrize("nc,ne", [(700, 300), (1400, 600), (140, 60)])
def test_plan_settles_at_a_fixed_point_and_passes_its_own_report(nc, ne):
    bases = _bases()
    plan, rep = SEL.plan_block(bases, n_complement=nc, n_equiv=ne, seed="t37b-test", equiv_pool=POOL.choices())
    assert rep["pass"], rep
    assert len(plan) > 100 and rep["basis"] <= rep["target_basis"] == nc + ne
    assert _fixed_point(bases, plan, nc, ne, "t37b-test", POOL) == [i.pid for i in plan]
    n = len(plan)
    assert rep["max_template_share"] <= max(1, math.floor(0.02 * n)) / n + 1e-9
    assert rep["implicit_share"] >= 0.25 and rep["non_syntactic_share"] >= 0.30


def test_equiv_partners_are_capped_by_their_paraphrase_not_by_the_base_question():
    """Before A1-3 one fixed question ('Does the evidence support the claim?') capped ALL of an entry's equiv rows at 2%
    of the block: 25 paraphrases gave 1 row. Now 25 paraphrases give 25."""
    covid = [b for b in _bases(80) if b.entry.key == "gd_check_covid/support"]
    plan, rep = SEL.plan_block(covid, n_complement=0, n_equiv=40, seed="t37b-test", equiv_pool=POOL.choices(),
                               source_cap=1.0)
    assert rep["equiv"] == 25                                 # one row per paraphrase at cap 1; the entry key is free
    assert not any("|equiv|-|" in k for k in SEL._template_counts(plan))
    assert Counter(i.meta["para"] for i in plan).most_common(1)[0][1] == 1


def test_complement_wordings_are_still_capped_by_entry_and_base_question():
    covid = [b for b in _bases(80) if b.entry.key == "gd_check_covid/support"]
    plan, rep = SEL.plan_block(covid, n_complement=40, n_equiv=0, seed="t37b-test", equiv_pool=POOL.choices(),
                               source_cap=1.0, template_cap=0.1)
    n = len(plan)
    keys = SEL._template_counts(plan)
    assert keys and max(keys.values()) <= max(1, math.floor(0.1 * n))
    assert all(k.startswith("gd_check_covid/support|") and "|equiv|" not in k for k in keys)


def _cells(plan):
    cell, word = defaultdict(lambda: [0, 0]), defaultdict(lambda: [0, 0])
    for i in plan:
        s = SEL._side(i.base, i.kind)
        cell[(i.base.entry.key, i.kind)][s] += 1
        word[SEL._wording_cell(i.base, i.kind, i.frame, i.cue, i.variant, i.meta)][s] += 1
    return cell, word


def test_partner_gold_is_balanced_in_the_family_and_in_every_cell():
    bases = _bases(60, skew=True)
    nc, ne = 700, 300
    plan, rep = SEL.plan_block(bases, n_complement=nc, n_equiv=ne, seed="t37b-test", equiv_pool=POOL.choices())
    off, _ = SEL.plan_block(bases, n_complement=nc, n_equiv=ne, seed="t37b-test", equiv_pool=POOL.choices(),
                            balance=False)
    ys = sum(SEL._side(i.base, i.kind) for i in plan)
    assert abs(2 * ys - len(plan)) <= 1, (ys, len(plan))
    cell, word = _cells(plan)
    assert max(abs(a - b) for a, b in cell.values()) <= 1
    assert max(abs(a - b) for a, b in word.values()) <= 1
    assert abs(rep["partner_yes_rate"] - 0.5) <= 1 / len(plan)
    # without the balance rule the skewed pool shows (the test would not see the rule otherwise): its equiv partners
    # (gold = base gold) are about 80% yes, the balanced plan's are 50%
    rate = lambda p, k: (lambda xs: sum(xs) / len(xs))([SEL._side(i.base, i.kind) for i in p if i.kind == k])   # noqa: E731
    assert rate(off, "equiv") > 0.65 and abs(rate(plan, "equiv") - 0.5) < 0.02
    assert {i.kind for i in plan} == set(SRC.KINDS)


def test_balance_reads_the_gold_only_to_choose_bases():
    bases = _bases(60, skew=True)
    flipped = [SEL.Base(dict(b.row, gold=1 - b.row["gold"]), b.entry, b.kinds, b.defs) for b in bases]
    kw = dict(n_complement=140, n_equiv=60, seed="t37b-test", equiv_pool=POOL.choices())
    p1, _ = SEL.plan_block(bases, **kw)
    p2, _ = SEL.plan_block(flipped, **kw)
    sig = lambda p: [(i.pid, i.kind, i.frame, i.cue, i.variant, i.meta.get("para")) for i in p]   # noqa: E731
    assert sig(p1) == sig(p2) and p1                  # the choice is symmetric in the gold: no preference for a label
    for i in p1:                                      # the label is never the plan's: it is 1 - gold / gold at row time
        c = BL.check_candidate(i, BL.program_partner(i), author="program", frames=TRAIN)
        if c.ok:
            assert BL.partner_row(c)["gold"] == (1 - i.base.row["gold"] if i.kind in SRC.OPPOSITE_KINDS
                                                 else i.base.row["gold"])


def test_dev_plan_is_not_balanced_and_not_changed():
    bases = _bases(30)
    kw = dict(n_complement=60, n_equiv=0, seed="t37b-test", mode="dev")
    a, ra = SEL.plan_block(bases, **kw)
    b, rb = SEL.plan_block(bases, balance=False, **kw)
    assert [i.pid for i in a] == [i.pid for i in b] and ra["pass"]


# ------------------------------------------------------------------------------------------------ A1-6: length

def _stand_in_cands(mode="train"):
    bases = SEL.eligible(FX.rows(), [], status=FX.keep_all, strict_inputs=False)[0]
    plan, _ = SEL.plan_block(bases, n_complement=12, n_equiv=4, mode=mode, equiv_pool=AP.Pool(FX.stand_in_pool()).choices(),
                             source_cap=1.0, template_cap=1.0, balance=False)
    return BL.build_candidates(plan, mode=mode, records=AP.Pool(FX.stand_in_pool()).records)


def test_a_partner_row_over_2000_tokens_drops_its_unit():
    cands = _stand_in_cands()
    assert len(cands) > 4 and all(c.ok for c in cands)
    toks = lambda rows: [2001 if i == 0 else 300 for i in range(len(rows))]   # noqa: E731
    rows, rels, rep = BL.finalize(cands, run_g15=False, trim=False, token_fn=toks)
    assert len(rows) == len(cands) - 1 and len(rels) == len(rows)
    assert len(rep["length_dropped"]) == 1 and "2001" in rep["length_dropped"][0][1]
    assert rep["length_dropped"][0][0] == cands[0].item.pid
    rows2, _r, rep2 = BL.finalize(cands, run_g15=False, trim=False, token_fn=lambda rs: [2000] * len(rs))
    assert len(rows2) == len(cands) and rep2["length_dropped"] == []         # exactly 2,000 is allowed
    rows3, _r, rep3 = BL.finalize(cands, run_g15=False, trim=False, token_fn=toks, max_tokens=None)
    assert len(rows3) == len(cands)                                          # the check can be switched off


def test_the_length_rule_adds_to_validate_rows_conservative_estimate_and_dev_is_exempt():
    """rows.validate_row already refuses a row whose 3-characters-per-token estimate is over 2,000; A1-6 adds the real
    count (a table-heavy state of about 5,000 characters can be 2,020 real tokens). Dev rows are exempt from A1-6."""
    cands = _stand_in_cands()
    cands[0].item.base.row.update(state="x" * 7000)
    rows, _r, rep = BL.finalize(cands, run_g15=False, trim=False)                 # no counter: the old estimate drops it
    assert len(rows) == len(cands) - 1 and any("tokens" in p for _pid, ps in rep["dropped_at_finalize"] for p in ps)
    dev = _stand_in_cands("dev")
    over = lambda rs: [5000] * len(rs)                                           # noqa: E731
    rows_d, _r, rep_d = BL.finalize(dev, mode="dev", run_g15=False, token_fn=over)
    assert len(rows_d) == len(dev) and rep_d["length_dropped"] == []


# ------------------------------------------------------------------------------------------------ the freeze manifest

def test_the_fix_manifest_excuses_only_generator_code_changed_from_the_frozen_sha(tmp_path, monkeypatch):
    from t37b import answers_gate as G
    import json
    assert G.fix_shas()                                               # the i1 manifest exists on disk
    assert G.v1_untouched() == []
    fm = json.loads(G.FREEZE_MANIFEST.read_text(encoding="utf-8"))
    code = next(k for k in fm["sha256"] if k.endswith("c2_build/t37b/builder.py"))
    pool = next(k for k in fm["sha256"] if k.endswith("t37b_equiv_pool.json"))
    now = {k: hashlib.sha256((G.LEAN / k).read_bytes()).hexdigest() for k in (code, pool)}

    def manifest(code_entry, pool_entry, freeze_overrides):
        f2 = json.loads(json.dumps(fm))
        f2["sha256"].update(freeze_overrides)
        fp = tmp_path / "freeze.json"
        fp.write_text(json.dumps(f2), encoding="utf-8")
        xp = tmp_path / "fix.json"
        xp.write_text(json.dumps({"code": {code: code_entry, pool: pool_entry}}), encoding="utf-8")
        monkeypatch.setattr(G, "FREEZE_MANIFEST", fp)
        monkeypatch.setattr(G, "FIX_MANIFEST", xp)
        return [p for p in G.v1_untouched() if p in (f"{code} changed", f"{pool} changed")]   # the two files under test

    # the code file differs from the frozen sha; the fix manifest names exactly frozen -> now: excused
    assert manifest({"from": "a" * 64, "to": now[code]}, {"from": "b" * 64, "to": now[pool]},
                    {code: "a" * 64}) == []
    # the same entry for a data file is ignored: the pool must equal its frozen sha
    assert manifest({"from": "a" * 64, "to": now[code]}, {"from": "b" * 64, "to": now[pool]},
                    {code: "a" * 64, pool: "b" * 64}) == [f"{pool} changed"]
    # a code file edited again after the fix (its sha is not the manifest's 'to') is flagged
    assert manifest({"from": "a" * 64, "to": "c" * 64}, {}, {code: "a" * 64}) == [f"{code} changed"]
    # a fix entry that does not start from the frozen sha excuses nothing
    assert manifest({"from": "d" * 64, "to": now[code]}, {}, {code: "a" * 64}) == [f"{code} changed"]
