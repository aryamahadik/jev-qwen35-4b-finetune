"""F7 decide2 (golden_src/gen3/v3_nested_negation.py) on the WRITTEN F7 rows: the three parse gaps the generator
repair agent reported (yn2b/F7_OBJECTIONS.md, R1) and the 100% agreement that precheck 2.3 needs. Read-only: run_files
returns predictions and a report and writes nothing.

R1.1  card rule 'each one either is toxic or is not' (copula batch) was not read -> 696 rows unparsed;
      the tail must fit the property ('is X or is not', 'Vs ... or does not'), else the line is refused.
R1.2  'Is it true that invoice X was never paid?' ('SUBJ be never R') had no negation peel -> 2 rows unparsed.
R1.3  'not one of the four comments ...' (count word after 'not one of the') was not read -> 4 probe rows, hidden
      behind R1.1; a count word must name the batch size.
Arbiter round 3 (yn2b/F7_OBJECTIONS.md):
A3    'no X other than X 4 ...' (universal / negative exceptive) when X 4 lacks the property: the literal set-minus
      reading and the exceptive (inclusion) reading differ -> decide2 refuses the row; existential exceptives stay
      literal (checklist item 31's example).
A4    'the opposite / reverse / contrary of a claim' over a universal claim on a mixed batch: plain denial and the
      contrary reading differ -> refused unless the card defines the word as plain denial. A quantifier inside a
      term definition ('the batch fails to count as tag K') is not counted.
devx  the round-2 devx parse table (r_f7x2_*), the AMBIG op (two readings, refused when they differ) and the check
      that a single base text's human label belongs to the text shown.
Arbiter round 4: the devx table covers the round-3 ids (r_f7x3_*) and binds every LF to the sha256 of the text it
      was written from; a devx row whose text differs is refused, whether or not its id changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import v3_nested_negation as v3  # noqa: E402

DV = LEAN / "data" / "v14_parts"
FILES = {k: DV / ("f7_%s.jsonl" % k) for k in ("train", "probe", "devx")}
# The behaviour tests below pin decide2 on named rows of the round-1 build (r1). Generator round 3 rebuilt F7, so row
# ids now name other rows, and the A3 / A4 ambiguous constructions are gone from the written files by design; the r1
# rows are read from the byte-for-byte backup. The 2.3 gate (test_written_rows_agree_100_percent) reads the written
# files.
R1 = DV / "f7_v2_r1_backup"
R1_FILES = {k: R1 / ("f7_%s.jsonl" % k) for k in ("train", "probe")}
pytestmark = pytest.mark.skipif(not all(p.exists() for p in FILES.values()), reason="F7 rows not written")


@pytest.fixture(scope="module")
def ctx():
    return v3.Ctx(LEAN)


@pytest.fixture(scope="module")
def rows():
    if not all(p.exists() for p in R1_FILES.values()):
        pytest.skip("round-1 F7 backup not present")
    out = {}
    for name in ("train", "probe"):
        with open(R1_FILES[name], encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                out[r["id"]] = r
    return out


def _row(rows, rid):
    if rid not in rows:
        pytest.skip(rid + " not in this build")
    return json.loads(json.dumps(rows[rid]))


def _swap(row, old, new, fields=("instructions", "card")):
    n = 0
    for k in fields:
        if row.get(k) and old in row[k]:
            n += row[k].count(old)
            row[k] = row[k].replace(old, new)
    assert n, "mutation did not apply: " + old
    return row


# ------------------------------------------------------------------------------------------------- R1.1
def test_copula_batch_rule_is_read(rows, ctx):
    r = _row(rows, "r_f7nn2_f7v2_ho_00098a_0")
    assert "each one either is toxic or is not" in r["card"]
    pred, notes = v3.decide2_row(r, ctx)
    assert pred is not None, notes
    assert pred == r["gold"]


def test_batch_rule_tail_must_fit_the_property(rows, ctx):
    r = _swap(_row(rows, "r_f7nn2_f7v2_ho_00098a_0"), "is toxic or is not", "is toxic or does not", ("card",))
    pred, notes = v3.decide2_row(r, ctx)
    assert pred is None and "batch rule tail" in notes[0], notes
    r = _row(rows, "r_f7nn2_f7v2_tr_00010a_0")
    assert "reports an actual crash or does not" in r["card"]
    assert v3.decide2_row(r, ctx)[0] == r["gold"]
    r = _swap(r, "reports an actual crash or does not", "reports an actual crash or is not", ("card",))
    pred, notes = v3.decide2_row(r, ctx)
    assert pred is None and "batch rule tail" in notes[0], notes


# ------------------------------------------------------------------------------------------------- R1.2
@pytest.mark.parametrize("rid", ["r_f7nn2_f7v2_tr_00289a_2", "r_f7nn2_f7v2_tr_00289b_2"])
def test_be_never_is_read_as_a_negation(rows, ctx, rid):
    r = _row(rows, rid)
    assert "was never paid" in r["instructions"]
    pred, notes = v3.decide2_row(r, ctx)
    assert pred is not None, notes
    assert pred == r["gold"]
    # 'never' is a negation, not noise: without it the answer flips (instruction and both card lines changed)
    m = _swap(json.loads(json.dumps(r)), "was never paid", "was paid")
    assert v3.decide2_row(m, ctx)[0] == 1 - r["gold"]


# ------------------------------------------------------------------------------------------------- R1.3
@pytest.mark.parametrize("rid", ["r_f7nn2_f7v2_ho_00367a_2", "r_f7nn2_f7v2_ho_00367b_2"])
def test_not_one_of_takes_a_count_word(rows, ctx, rid):
    r = _row(rows, rid)
    assert "not one of the four comments" in r["instructions"]
    pred, notes = v3.decide2_row(r, ctx)
    assert pred is not None, notes
    assert pred == r["gold"]
    # the count word must name the batch size
    m = _swap(json.loads(json.dumps(r)), "not one of the four comments", "not one of the five comments")
    pred, notes = v3.decide2_row(m, ctx)
    assert pred is None, (pred, notes)


# ------------------------------------------------------------------------------------------------- A3 exceptives
def test_negative_exceptive_refused_when_excepted_item_lacks_the_property(ctx):
    r = _row(_probe_rows(), "r_f7nn2_f7v2_ho_00382a_3")
    assert "no comment other than Comment 4 is toxic" in r["instructions"]
    pred, notes = v3.decide2_row(r, ctx)
    assert pred is None and "AMBIGUOUS: exceptive" in notes[0], (pred, notes)


def test_negative_exceptive_read_when_inclusion_holds(rows, ctx):
    # Complaint 2 reports a fire and no other complaint does: both readings agree, so the row is read
    r = _row(rows, "r_f7nn2_f7v2_tr_00033a_1")
    assert "not a single complaint other than Complaint 2" in r["instructions"]
    pred, notes = v3.decide2_row(r, ctx)
    assert pred is not None and pred == r["gold"], notes


def test_existential_exceptive_stays_literal(rows, ctx):
    # 'some complaint other than Complaint 2 ...' carries no inclusion condition (checklist item 31 example)
    r = _row(rows, "r_f7nn2_f7v2_tr_00033a_0")
    assert "some complaint other than Complaint 2" in r["instructions"]
    pred, notes = v3.decide2_row(r, ctx)
    assert pred is not None and pred == r["gold"], notes


# ------------------------------------------------------------------------------------------------- A4 frame words
WORDING = "- wording: here 'the %s of a claim' means its plain denial: the %s holds exactly when the claim itself fails"


def test_opposite_of_universal_claim_on_mixed_batch_refused(rows, ctx):
    r = _row(rows, "r_f7nn2_f7v2_tr_00372b_4")
    assert "the opposite of a claim" in r["instructions"] and "not a single request" in r["instructions"]
    pred, notes = v3.decide2_row(r, ctx)
    assert pred is None and "AMBIGUOUS: 'opposite'" in notes[0], (pred, notes)
    # the card's plain-denial definition settles the reading
    m = json.loads(json.dumps(r))
    m["card"] = m["card"].replace("\n- note: the batch settles", "\n" + WORDING % ("opposite", "opposite")
                                  + "\n- note: the batch settles")
    assert "'the opposite of a claim' means its plain denial" in m["card"]
    pred, notes = v3.decide2_row(m, ctx)
    assert pred is not None and pred == r["gold"], notes


def test_defined_contrary_is_read_and_undefined_contrary_is_refused(ctx):
    r = _row(_probe_rows(), "r_f7nn2_f7v2_ho_00367b_2")
    assert "'the contrary of a claim' means its plain denial" in r["card"]
    pred, notes = v3.decide2_row(r, ctx)
    assert pred is not None and pred == r["gold"], notes
    m = json.loads(json.dumps(r))
    m["card"] = "\n".join(x for x in m["card"].split("\n") if not x.startswith("- wording:"))
    pred, notes = v3.decide2_row(m, ctx)
    assert pred is None and "AMBIGUOUS: 'contrary'" in notes[0], (pred, notes)


def test_quantifier_inside_a_term_definition_is_not_counted(rows, ctx):
    # 'the reverse of the claim that the batch fails to count as 'tag K'': a yes/no claim about the batch
    r = _row(rows, "r_f7nn2_f7v2_tr_01052b_2")
    assert "neither Narrative 1 nor Narrative 3" in r["card"]
    pred, notes = v3.decide2_row(r, ctx)
    assert pred is not None and pred == r["gold"], notes


# ------------------------------------------------------------------------------------------------- devx table
@pytest.fixture(scope="module")
def devx_rows():
    with open(FILES["devx"], encoding="utf-8") as f:
        return {r["id"]: r for r in (json.loads(x) for x in f)}


def test_devx_parse_table_covers_the_round2_ids(devx_rows):
    table = json.loads(v3.DEVX_LF.read_text())
    assert set(table["rows"]) == set(devx_rows)
    assert {r["meta"]["ladder_id"] for r in devx_rows.values()} == set(table["ladders"])
    # arbiter round 4: every LF is bound to the exact text of the written row
    assert set(table["text_sha256"]) == set(devx_rows)
    assert all(table["text_sha256"][i] == v3.devx_text_sha(r) for i, r in devx_rows.items())


@pytest.mark.parametrize("field,old,new", [
    ("card", "\n- note: here 'the opposite' of a claim means its plain negation.", ""),   # drop the A4 definition
    ("instructions", "not a single comment is toxic", "a single comment is toxic"),     # drop one negation
])
def test_devx_stale_lf_refused_when_the_text_changes(devx_rows, ctx, field, old, new):
    # arbiter round 4: the table was keyed by id only, so a rewrite that kept its id reused a stale LF silently.
    ev = v3.DevxEval(ctx)
    r = json.loads(json.dumps(devx_rows["r_f7x3_14a_3"]))
    assert ev.decide(r) == r["gold"]                      # control: the written text is read
    assert old in r[field]
    r[field] = r[field].replace(old, new)
    with pytest.raises(v3.ParseError, match="differs from the text its LF was written from"):
        ev.decide(r)


R2 = DV / "f7_devx_r2_backup"


@pytest.mark.skipif(not (R2 / "f7_devx_decide2_lf_arb3.json").exists(), reason="round-2 devx backup not present")
def test_devx_ambig_refuses_only_when_readings_differ(ctx):
    # The two rows were rewritten in devx round 3 (new ids r_f7x3_*), so the AMBIG op is pinned on the round-2 rows
    # and the arbiter-round-3 parse table, both kept in data/v14_parts/f7_devx_r2_backup/.
    with open(R2 / "f7_devx.jsonl", encoding="utf-8") as f:
        old = {r["id"]: r for r in (json.loads(x) for x in f)}
    ev = v3.DevxEval(ctx)
    ev.table = json.loads((R2 / "f7_devx_decide2_lf_arb3.json").read_text())
    # arbiter round 4: bind that table to the round-2 text it was written from (it predates text_sha256)
    ev.table["text_sha256"] = {i: v3.devx_text_sha(r) for i, r in old.items()}
    with pytest.raises(v3.Ambiguous):
        ev.decide(old["r_f7x2_17b_1"])                   # Post 3 is not a Language post: readings differ
    r = old["r_f7x2_17a_1"]                               # Post 2 is a Language post: both readings say no
    assert ev.decide(r) == r["gold"]


def test_devx_single_text_label_must_belong_to_the_shown_text(devx_rows, ctx):
    ev = v3.DevxEval(ctx)
    r = json.loads(json.dumps(devx_rows["r_f7x2_01a_0"]))
    assert ev.decide(r) == r["gold"]
    r["state"] = devx_rows["r_f7x2_01b_0"]["state"]      # the twin's text under this ladder's base id
    with pytest.raises(v3.ParseError, match="does not match its base"):
        ev.decide(r)


def _probe_rows():
    if not R1_FILES["probe"].exists():
        pytest.skip("round-1 F7 backup not present")
    out = {}
    with open(R1_FILES["probe"], encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            out[r["id"]] = r
    return out


# ------------------------------------------------------------------------------------------------- 2.3 target
@pytest.fixture(scope="module")
def run(ctx):
    metas = {k: str(DV / ("f7_%s_meta.jsonl" % k if k != "train" else "f7_meta.jsonl")) for k in FILES}
    return v3.run_files({k: str(p) for k, p in FILES.items()}, ctx, metas)


@pytest.mark.parametrize("name", ["train", "probe", "devx"])
def test_written_rows_agree_100_percent(run, name):
    rep = run[1][name]
    assert rep["unparsed"] == 0, rep["unparsed_rows"][:5]
    assert rep["disagree"] == 0, rep["disagreements"][:5]
    assert rep["agree"] == rep["rows"] > 0
