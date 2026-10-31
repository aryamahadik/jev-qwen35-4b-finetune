"""The F6 decide2 on the WRITTEN rows (data/v14_parts/yn2b_raw/[dev/]gen3_def_literal.jsonl): SPEC 8.1 agreement
through mv_core.verify_labels, 8.3 structure under decide2 alone, fact parity across views, no item with two
sufficient reasons, cards that say what the question asks, and mutation checks that decide2 really follows the
facts and the record (not vacuous). Read-only."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))

import dl_packs as P  # noqa: E402  (surface data only)
import mv_core as mv  # noqa: E402
import v3_def_literal as v3  # noqa: E402

pytestmark = pytest.mark.skipif(not (v3.RAW / f"{v3.KEY}.jsonl").exists(), reason="F6 raw rows not written")


@pytest.fixture(scope="module")
def parts():
    out = {}
    for part in ("train", "dev"):
        rows = v3.load_rows(part)
        out[part] = (rows, v3.load_rels(part), v3.agreement(rows))
    return out


def test_every_row_parses_and_agrees_100(parts):
    for part, (rows, _, ag) in parts.items():
        assert not [d for d in ag["disagreements"] if d["error"]], (part, ag["disagreements"][:3])
        assert ag["agree"] == ag["rows"] == len(rows), (part, ag["disagreements"][:5])


def test_official_verify_labels(parts):
    for part, (rows, _, _) in parts.items():
        rep = mv.verify_labels(rows, lambda r: v3.decide2_row({**r, "_defs": mv.load_defs(v3.KEY, r["meta"]["defs"])}))
        assert rep["ok"] and rep["rows"] == len(rows), (part, rep)


def test_counts_match_the_build_report(parts):
    assert len(parts["train"][0]) == 1650 and len(parts["dev"][0]) == 150


def test_structure_under_decide2(parts):
    for part, (rows, rels, ag) in parts.items():
        st = v3.structure_under_decide2(rows, rels, ag["answers"])
        assert st["contrast_pairs"] > 0 and not st["contrast_not_flipped"], part
        assert not st["complement_not_inverted"] and not st["equiv_changed"] and not st["inv_changed"], part
        assert not st["unknown_rel"] and not st["fact_parity_broken"], (part, st["fact_parity_broken"][:3])
        # a contrast twin changes exactly one fact (element twin) or only the definition (exclusion twin)
        assert set(st["contrast_fact_changes"]) <= {"1 fact(s)", "0 fact(s) + definition"}, st["contrast_fact_changes"]


def test_no_item_has_two_sufficient_reasons(parts):
    for part, (rows, _, _) in parts.items():
        rr = v3.reasons_report(rows)
        assert not rr["two_reasons_yes"] and not rr["two_reasons_no"], (part, rr["two_reasons_yes"][:3],
                                                                       rr["two_reasons_no"][:3])


def test_cards_and_crosschecks(parts):
    for part, (rows, _, _) in parts.items():
        assert v3.card_report(rows)["card_question_mismatch"] == [], part
        cc = v3.crosscheck_report(rows)
        assert not cc["pack_mismatch"] and not cc["fmt_mismatch"], part


def test_default_readings_are_the_ones_the_gold_follows(parts):
    """Every alternative reading that changes an answer moves it AWAY from the gold (none is silently relied on)."""
    for part, (rows, _, ag) in parts.items():
        for name, s in v3.sensitivity(rows, ag["answers"]).items():
            if name.startswith("distractor:"):
                assert s["changed"] > 0               # the outside rule is a live distractor
            else:
                assert s["gold_follows_alt"] == 0, (part, name, s)


# ------------------------------------------------------------------------------------------------ mutations
def _toggle(rec: str) -> str:
    return rec[4:] if rec.startswith("not ") else f"not {rec}"


def _swap_record(state: str, fmt: str, rec: str) -> str:
    new = _toggle(rec)
    pats = {"json": (f'"recorded classification": "{rec}"', f'"recorded classification": "{new}"'),
            "kv": (f"file.recorded classification: {rec}\n", f"file.recorded classification: {new}\n"),
            "markdown": (f"- recorded classification: {rec}\n", f"- recorded classification: {new}\n"),
            "email": (f"Recorded classification for this file: {rec}.", f"Recorded classification for this file: {new}."),
            "prose": None}
    if fmt == "prose":
        out, n = re.subn(r"(records the [a-z]+ as )" + re.escape(rec) + r"\.", lambda m: f"{m.group(1)}{new}.", state)
        assert n == 1, rec
        return out
    a, b = pats[fmt]
    assert state.count(a) == 1, (fmt, a)
    return state.replace(a, b)


def test_mutation_judge_record_flip_flips_the_answer(parts):
    n = 0
    for part, (rows, _, ag) in parts.items():
        for r in rows:
            if r["meta"]["qkind"] != "yn" or not r["meta"]["tpl"].startswith("judge"):
                continue
            doc = v3.parse_state(r["state"])
            r2 = dict(r, state=_swap_record(r["state"], doc.fmt, doc.record))
            assert v3.decide2_row(r2) == ("no" if ag["answers"][r["rid"]] == "yes" else "yes"), r["rid"]
            n += 1
    assert n > 300


def _satisfy(c: v3.Cond) -> int:
    return {">=": c.limit, ">": c.limit + 1, "<=": c.limit, "<": c.limit - 1}[c.op]


def test_mutation_fixing_the_single_failing_number_flips_no_to_yes(parts):
    """kv yes/no 'is' rows whose only reason for 'no' is one numeric element: set that value to the nearest value that
    meets the element, re-render the one kv line, and decide2 must flip (and the opposite move for 'yes' rows decided
    by a single numeric element under AND)."""
    flipped = 0
    for part, (rows, _, ag) in parts.items():
        for r in rows:
            if r["meta"]["fmt"] != "kv" or r["meta"]["qkind"] != "yn":
                continue
            o = v3.solve(r)
            if o["q"]["family"] != "is":
                continue
            d, oc = o["defn"], o["outcome"]
            if oc.applies or oc.reasons_no != 1 or any(x[2] for x in oc.excl) or oc.deem_ok:
                continue
            cands = [c for c, ok in zip(d.elements, oc.elements) if not ok and c.kind == "num" and
                     o["facts"].get(c.attr) is not None]
            if d.joiner == "all" and len(cands) != 1:
                continue
            if not cands:
                continue
            c = cands[0]
            a = P.PACKS[d.pack].attr(c.attr)
            old = f"{d.entity}.{a.label}: {P.fmt_unit(a.unit, o['facts'][c.attr])}\n"
            new = f"{d.entity}.{a.label}: {P.fmt_unit(a.unit, _satisfy(c))}\n"
            assert r["state"].count(old) == 1, r["rid"]
            r2 = dict(r, state=r["state"].replace(old, new))
            before = ag["answers"][r["rid"]]
            assert v3.decide2_row(r2) == ("yes" if before == "no" else "no"), (r["rid"], old, new)
            flipped += 1
    assert flipped >= 20


def test_mutation_garbled_sentence_is_refused(parts):
    rows = [r for r in parts["train"][0] if r["meta"]["fmt"] == "prose"][:50]
    for r in rows:
        paras = r["state"].split("\n\n")
        paras[1] += " The weather was pleasant."
        assert v3.decide2_row(dict(r, state="\n\n".join(paras))) is mv.UNDEFINED, r["rid"]


def test_agreement_record_matches_the_data():
    p = LEAN / "yn2b" / "v3_def_literal_agreement.json"
    if not p.exists():
        pytest.skip("agreement record not written yet")
    rep = json.loads(p.read_text())
    for part, inp in rep["inputs"].items():
        assert hashlib.sha256((LEAN / inp["path"]).read_bytes()).hexdigest() == inp["sha256"], part
        assert rep["parts"][part]["agree"] == rep["parts"][part]["rows"] == inp["rows"], part
