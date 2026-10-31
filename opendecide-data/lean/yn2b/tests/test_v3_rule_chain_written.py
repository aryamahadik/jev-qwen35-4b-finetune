"""The F1 decide2 on the WRITTEN rows (data/v14_parts/yn2b_raw/[dev/]gen3_rule_chain.jsonl): SPEC 8.1 agreement
(100% on train and dev), 8.3 structure under decide2 alone, the reading/probe sensitivity, and decide2's independence
from the generator. Read-only (write_agreement goes to tmp_path and the redirected manifest)."""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from v3f1_helpers import v3

pytestmark = pytest.mark.skipif(not (v3.RAW / f"{v3.KEY}.jsonl").exists(), reason="F1 raw rows not written")


@pytest.fixture(scope="module")
def parts():
    out = {}
    for split in ("train", "dev"):
        rows = v3.load_rows(split)
        out[split] = (rows, v3.load_rels(split), v3.agreement(rows))
    return out


def test_every_row_parses(parts):
    for split, (rows, _, ag) in parts.items():
        errs = [d for d in ag["disagreements"] if d["error"]]
        assert not errs, f"{split}: {errs[:5]}"


@pytest.mark.parametrize("split", ["train", "dev"])
def test_agreement_is_100_percent(parts, split):
    rows, _, ag = parts[split]
    assert ag["agree"] == ag["rows"] == len(rows), ag["disagreements"][:5]


def test_structure_under_decide2(parts):
    for split, (rows, rels, ag) in parts.items():
        st = v3.structure_under_decide2(rows, rels, ag["answers"])
        assert st["ok"], (split, {k: x for k, x in st.items() if isinstance(x, list) and x})
        assert st["contrast_pairs"] > 0 and st["equiv"] > 0 and st["complement"] > 0 and st["inv"] > 0


def test_mv_core_verify_labels_api(parts):
    import mv_core
    for split, (rows, _, _) in parts.items():
        rep = mv_core.verify_labels(rows, v3.decide2_row)
        assert rep["ok"] and rep["disagree"] == 0 == rep["undefined"], (split, rep)


def test_gold_never_follows_an_alternative_reading_or_a_probe(parts):
    rows, _, ag = parts["train"]
    se = v3.sensitivity(rows, ag["answers"])
    for name, x in se.items():
        assert x["gold_follows_alt"] == 0, (name, x["rids"][:5])
    # the probes show the data exercises each mechanism decide2 agrees on
    for name in v3.PROBES:
        assert se[name]["changed"] > 0, name
    # the readings that change answers at all (the ambiguity list in the report) stay small
    assert se["decisive_outcome=code+amount"]["changed"] <= 4
    assert se["business_limit=count"]["changed"] <= 8


def test_no_notes_and_text_matches_meta(parts):
    for split, (rows, _, ag) in parts.items():
        assert v3.notes_report(rows, ag["infos"]) == {}, split
        assert v3.meta_crosscheck(rows, ag["infos"])["mismatch"] == [], split


def test_cards_say_what_yes_means_for_the_question_read(parts):
    for split, (rows, _, ag) in parts.items():
        cr = v3.card_report(rows, ag["infos"])
        assert cr["yn_rows_checked"] > 0 and cr["card_question_mismatch"] == [], (split, cr["card_question_mismatch"][:5])


def test_every_decisive_question_has_exactly_one_decisive_clause(parts):
    for split, (rows, _, ag) in parts.items():
        n = 0
        for r in rows:
            info = ag["infos"][r["rid"]]
            if info["q"] == "dec":
                n += 1
                assert len(info["pivotal_all"]) == 1, r["rid"]
        assert n > 0


BRIEF = {"f1-tr-000185-0": "yes", "f1-tr-000641-0": "Section 2.2 (signed leave form requirement)",
         "f1-tr-000293-1": "yes", "f1-tr-001194-1": "no",
         "f1-dh-000051-1": ('Under the fee code, the outcome of this application is some other outcome than "waiver '
                            'refused - registration certificate missing".')}
BRIEF_ROWS = Path(__file__).resolve().parent / "f1_brief_rows.json"


def test_the_five_hand_read_rows_of_the_f1_brief():
    """R2 (1 Oct) regenerated F1, so the rids now name other items: the five hand-read rows are frozen in
    f1_brief_rows.json (text, card and the hand-read answer only) and decide2 reads them from there."""
    fx = json.loads(BRIEF_ROWS.read_text())["rows"]
    assert {x["rid"]: x["want"] for x in fx} == BRIEF
    cards = {x["meta"]["defs"]: x["card"] for x in fx if x["meta"]["defs"]}
    v3.set_card_lookup(cards.get)
    try:
        for x in fx:
            assert v3.decide2_row({k: x[k] for k in ("rid", "key", "state", "instructions", "options", "meta")}) \
                == x["want"], x["rid"]
    finally:
        v3.set_card_lookup(None)


def test_decide2_is_deterministic_and_reads_no_gold(parts):
    rows, _, ag = parts["dev"]
    for r in rows:
        r2 = {**r, "gold": None, "meta": {"defs": r["meta"].get("defs")}}   # gold and every other meta field hidden
        assert v3.decide2_row(r2) == ag["answers"][r["rid"]]


def test_independent_of_the_generator():
    src = Path(v3.__file__).read_text()
    for mod in ("gen3_rule_chain", "rc_core", "rc_render", "rc_numeric", "rc_repair", "rc_gen2"):
        assert not re.search(rf"^\s*(import|from)\s+{mod}\b", src, re.M), mod
    imports = set(re.findall(r"^\s*(?:import|from)\s+(\w+)", src, re.M))
    assert imports <= {"__future__", "csv", "datetime", "io", "json", "re", "sys", "dataclasses", "fractions",
                       "functools", "pathlib", "rc_skins", "mv_core", "yn2b_common", "argparse", "hashlib",
                       "collections"}, imports
    code = src.split('"""', 2)[2]
    body = code.split("\ndef solve(")[1].split("\ndef ", 1)[0]
    for fn in ("solve_f1a", "solve_nb", "nb_card"):
        body += code.split(f"\ndef {fn}(")[1].split("\ndef ", 1)[0]
    for token in ('["gold"]', "['gold']", '"edge"', '"tier"', '"shortcut', '"pack"', '"tpl"', '"view"'):
        assert token not in body, token


def test_write_agreement_goes_to_the_given_path_and_the_redirected_manifest(tmp_path, _tmp_manifest):
    out = tmp_path / "agree.json"
    rep = v3.write_agreement(out, probes=False)
    got = json.loads(out.read_text())
    assert got["parts"]["dev"]["disagree"] == 0 == rep["parts"]["train"]["disagree"]
    recs = [json.loads(x) for x in _tmp_manifest.read_text().splitlines()]
    assert len(recs) == 1 and recs[0]["part"] == "decide2_agreement" and recs[0]["path"].endswith("agree.json")
