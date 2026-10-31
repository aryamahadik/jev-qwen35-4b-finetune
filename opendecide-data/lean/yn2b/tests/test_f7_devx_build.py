"""Tests of the blind F7 devx v2 (yn2b/f7_devx_build.py, yn2b/f7_devx_audit.py). CPU only; reads the written devx
files and writes nothing outside pytest's tmp_path.

Each test pins one of the arbiter rulings on the round-1 devx (yn2b/F7_OBJECTIONS.md, O2 and arbiter round 2):
1.2 choice contract + antonym_gold, 1.4 look-alikes / rule words / reported content, 3.3 tags, 4.1c / 4.2c balance,
5.l restatement, 7.1 X12, 8.3 / 8.4 / 8.6 / 8.14 decontamination (the slow part runs in the audit with --decontam),
9.3 / 9.5 / 9.6 ladder semantics, 10.8 golden_train states.
"""
from __future__ import annotations

import collections
import json
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
DV = LEAN / "data/v14_parts"


def load(p):
    return [json.loads(x) for x in open(p, encoding="utf-8") if x.strip()]


@pytest.fixture(scope="module")
def written():
    return (load(DV / "f7_devx.jsonl"), load(DV / "f7_devx_meta.jsonl"), load(DV / "f7_devx_relations.jsonl"),
            load(LEAN / "yn2b/f7_devx_blind_packet.jsonl"))


@pytest.fixture(scope="module")
def built():
    import f7_devx_build as B
    return B.build(B.gold_positions(B.build()[1]))


@pytest.fixture(scope="module")
def audit(tmp_path_factory):
    import shutil
    import f7_devx_audit as A
    d = tmp_path_factory.mktemp("devx")
    for f in ("f7_devx.jsonl", "f7_devx_meta.jsonl", "f7_devx_relations.jsonl"):
        shutil.copy(DV / f, d / f)
    code = A.main(["--dir", str(d)])
    return code, json.loads((d / "f7_devx_audit.json").read_text())


def test_written_files_equal_a_fresh_build(written, built):
    for got, want in zip(written, built):
        assert [json.dumps(x, sort_keys=True) for x in got] == [json.dumps(x, sort_keys=True) for x in want]


def test_audit_passes_every_check(audit):
    code, out = audit
    assert code == 0 and out["_verdict"]["pass"], out["_verdict"]["failed"]
    assert out["_verdict"]["checks"] >= 45


@pytest.mark.parametrize("key", ["A.1.2", "A.1.3", "A.1.4", "A.2.1", "A.2.2", "A.2.4", "A.2.5", "A.2.6", "A.3.3",
                                 "A.4.1c", "A.4.2c", "A.5.l", "A.7.1", "A.8.9", "A.9.3", "A.9.5", "A.9.6"])
def test_ship_audit_row_checks_pass_on_devx(audit, key):
    assert audit[1][key]["pass"], audit[1][key]


def test_choice_rows_follow_the_lf_contract(written):
    """1.2: CHOICE at the root, select cue on the CHOICE node, one CORE per option, int gold index."""
    rows, metas, _, _ = written
    M = {m["id"]: m for m in metas}
    for r in rows:
        if r["qtype"] != "choice":
            continue
        m = M[r["id"]]
        lf = m["lf"]
        assert lf["op"] == "CHOICE" and isinstance(m["gold"], int) and r["options"][m["gold"]] == r["gold"]
        assert (lf["select"] == "false") == isinstance(lf.get("cue"), int)
        assert all(json.dumps(o).count('"op": "CORE"') == 1 for o in lf["options"])


def test_item21_rows_carry_antonym_gold_and_c7_bites(written):
    rows, metas, _, _ = written
    it21 = [m for m in metas if 21 in m["phen"]]
    assert it21 and all(m["qtype"] == "noul" and m["antonym_gold"] in (0, 1) for m in it21)
    assert sum(1 for m in it21 if m["antonym_gold"] != m["gold"]) / len(it21) >= 0.30


def test_lookalikes_sit_on_no_node_and_reported_negations_are_not_cues(written):
    """1.4: a look-alike is a cue on no node; a negation inside reported content is an information field only;
    rule words ('must not', 'unless', 'need not') are NOT nodes."""
    _, metas, _, _ = written

    def refs(n, acc):
        if isinstance(n.get("cue"), int):
            acc.append(n["cue"])
        for k in ([n["child"]] if "child" in n else []) + n.get("children", []) + n.get("options", []):
            refs(k, acc)
        return acc
    for m in metas:
        rs = collections.Counter(refs(m["lf"], []))
        for i, c in enumerate(m["cues"]):
            assert rs[i] == (0 if c["cls"] == "lookalike" else 1), (m["id"], c)
            assert "in_atom" not in c and "in_rule" not in c
        assert m["n_distractor"] == sum(1 for i, c in enumerate(m["cues"]) if c["cls"] != "lookalike"
                                        and not c["scoping"])
    assert any(m.get("content_negations") for m in metas)


def test_ar_rows_have_no_cue_word_and_a_null_not(written):
    """9.6: an AR row is NOT(cue null) with no cue word, plus an odd sibling of the same gold."""
    _, metas, _, _ = written
    ars = [m for m in metas if m["rung"] == "AR"]
    assert len(ars) >= 6
    for m in ars:
        assert not [c for c in m["cues"] if c["cls"] != "lookalike"] and m["depth"] == 1
        assert '"cue": null' in json.dumps(m["lf"])


def test_every_ladder_has_both_golds_and_r0(written):
    """9.5 and CL:215 (R0 in 100% of dev ladders)."""
    rows, metas, _, _ = written
    lad = collections.defaultdict(list)
    for r, m in zip(rows, metas):
        lad[m["ladder_id"]].append((r, m))
    for lid, rs in lad.items():
        assert {r["gold"] for r, m in rs if r["qtype"] == "noul"} == {0, 1}, lid
        assert sum(1 for _, m in rs if m["rung"] == "R0") >= 1 and len(rs) <= 5, lid


def test_twins_ask_the_same_questions_with_opposite_golds(written):
    rows, _, _, _ = written
    byq = collections.defaultdict(list)
    for r in rows:
        if r["qtype"] == "noul":
            byq[(r["meta"]["pair"], r["instructions"], r["card"])].append(r["gold"])
    assert len(byq) == 88 and all(sorted(v) == [0, 1] for v in byq.values())


def test_yes_lines_restate_question_side_distractors(written):
    """5.l: a format or side-clause distractor in the question is restated in the yes line."""
    rows, metas, _, _ = written
    for r, m in zip(rows, metas):
        yes = [ln for ln in (r["card"] or "").split("\n") if ln.lower().startswith("- yes: ")]
        if not yes or "no:" not in (r["card"] or "").lower():
            continue
        for c in m["cues"]:
            if c["position"] in ("outer_frame", "inner_claim", "separate_sentence") and c["cls"] != "lookalike" \
                    and not c["lexeme"].startswith("-") and not c["lexeme"].endswith("-"):
                lex = c["lexeme"].lower()
                assert lex.split()[0] in yes[0].lower() or lex == "n't" or lex in ("fail", "contradict", "refute",
                                                                                    "lack", "dispute", "reject",
                                                                                    "dismiss"), (r["id"], lex)


def test_at_most_two_cues_per_clause_position(written):
    """7.1 X12 proxy: <= 2 cues at each of inner_claim / outer_frame / separate_sentence / answer_map."""
    _, metas, _, _ = written
    for m in metas:
        pc = collections.Counter(c["position"] for c in m["cues"] if c["cls"] != "lookalike")
        assert all(pc[p] <= 2 for p in ("inner_claim", "outer_frame", "separate_sentence", "answer_map")), m["id"]


def test_base_texts_overlap_nothing(written):
    """10.8 / 8.1 / 8.2 / 10.6: every real base text has 0 word 8-grams in golden_train and in F7 train / probe
    states, and 0 12-grams in the ship audit's reference sets (yn2b/f7_devx_pool_scan.py)."""
    rows, _, _, _ = written
    flags = json.loads((LEAN / "yn2b/f7_devx_pool_flags.json").read_text())["flags"]
    refs = {ref for r in rows for ref in r["meta"]["orig"] if not ref.startswith("invented:")}
    assert refs == set(flags)
    for k, v in flags.items():
        assert not any(v[x] for x in ("golden_hits", "f7_hits", "infam_hits", "strict_hits", "infam_y_hits")), k


def test_blind_packet_hides_gold(written):
    rows, _, _, packet = written
    assert [p["id"] for p in packet] == [r["id"] for r in rows]
    assert all(set(p) == {"id", "ladder_id", "orig", "qtype", "state", "instructions", "card", "options"}
               for p in packet)


def test_round2_ids_cannot_match_the_stale_round1_parse_table(written):
    """The round-1 devx ids (r_f7x_*) are gone, so decide2's round-1 devx LF table cannot silently match a
    rewritten row; the devx LFs must be re-authored blind (2.3b exception). Round 3 rewrote 4 rows (A3 / A4); they
    carry r_f7x3_ ids for the same reason."""
    rows, _, _, _ = written
    assert all(r["id"].startswith(("r_f7x2_", "r_f7x3_")) for r in rows)
    assert not any(r["id"].startswith("r_f7x_") for r in rows)


ROUND3 = {"r_f7x3_14a_3": "r_f7x2_14a_3", "r_f7x3_14b_3": "r_f7x2_14b_3", "r_f7x3_17a_1": "r_f7x2_17a_1",
          "r_f7x3_17b_1": "r_f7x2_17b_1"}
R2 = DV / "f7_devx_r2_backup"


@pytest.mark.skipif(not (R2 / "f7_devx.jsonl").exists(), reason="round-2 devx backup not present")
def test_round3_rewrites_exactly_the_four_ambiguous_rows(written):
    """Arbiter round 3 (A3 pair 17, A4 pair 14): only those 4 rows change, every other row and sidecar line is byte
    for byte the round-2 row (so its blind-written decide2 LF still applies), and every rewritten row has a new id
    (so the round-2 LF of the old wording cannot match it)."""
    rows, metas, rels, _ = written
    old_rows, old_metas = load(R2 / "f7_devx.jsonl"), load(R2 / "f7_devx_meta.jsonl")
    assert len(rows) == len(old_rows) == 220
    changed = 0
    for new, old in zip(rows, old_rows):
        if new["id"] in ROUND3:
            changed += 1
            assert ROUND3[new["id"]] == old["id"]
            assert (new["instructions"], new["card"]) != (old["instructions"], old["card"])
            assert new["state"] == old["state"] and new["gold"] == old["gold"]
        else:
            assert json.dumps(new, sort_keys=True) == json.dumps(old, sort_keys=True)
    assert changed == 4
    for new, old in zip(metas, old_metas):
        if new["id"] not in ROUND3:
            assert json.dumps(new, sort_keys=True) == json.dumps(old, sort_keys=True)
    ids = {r["id"] for r in rows}
    assert all(x["a"] in ids and x["b"] in ids for x in rels)


def test_pair17_exceptive_has_one_reading_in_both_twins(written):
    """A3: 'no post apart from Post 3 belongs at either of the Language and Mathematics desks' also says that
    Post 3 belongs at one of them (inclusion). Post 3's human label must be one of the asked desks in both twins,
    so the literal (set-minus) and the exceptive readings agree."""
    import re
    rows, _, _, _ = written
    import f7_devx_build as B
    hit = [r for r in rows if "apart from Post 3" in r["instructions"] and r["qtype"] == "noul"]
    assert len(hit) == 2 and {r["meta"]["pair"] for r in hit} == {"f7x2_P17"}
    for r in hit:
        asked = re.findall(r"\b(Language|Science|Mathematics|Humanities)\b", r["instructions"].split("belongs at")[1])
        post3 = B.RAW[r["meta"]["orig"][2]][1]
        assert post3.split()[0] in asked, (r["id"], post3, asked)


def test_opposite_of_a_universal_batch_claim_is_defined_in_the_card(written):
    """A4: 'the opposite / reverse of a claim' with a universal quantifier over a batch has a plain-denial and a
    contrary reading; every such devx row defines the word in its card."""
    import re
    rows, metas, _, _ = written
    M = {m["id"]: m for m in metas}
    univ = re.compile(r"\b(?:not a single|none|no|every|all|each|only|neither)\b", re.I)
    n = 0
    for r in rows:
        ins = r["instructions"]
        w = re.search(r"\b(opposite|reverse|contrary)\b", ins)
        if not w or M[r["id"]]["ladder_kind"] != "multitext":
            continue
        claim = re.search(r"Claim: (.+?)\.", ins)
        if not claim or not univ.search(claim.group(1)):
            continue
        n += 1
        assert re.search(r"'the %s' of a claim means its plain (?:negation|denial)" % w.group(1), r["card"] or ""), \
            r["id"]
    assert n >= 2
