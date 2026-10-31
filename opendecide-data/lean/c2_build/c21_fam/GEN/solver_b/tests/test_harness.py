"""The A-versus-B harness itself: it must catch planted errors, and B must be deterministic."""
import copy

import agree_ab as H


def _rows(n=6):
    return H.build_rows("harness-test", n, "train")


def test_harness_counts_a_flipped_label_as_a_mismatch():
    rows = _rows()
    for r in rows:
        r["label"] = (r["label"] + 1) % r["k"]          # plant: A's answer is now wrong everywhere
    per_form, ans, parse, _ = H.run(rows)
    mism = sum(c["answer_mismatch"] for c in per_form.values())
    ok = sum(c["agree"] for c in per_form.values())
    assert ok == 0 and mism == len(rows)


def test_harness_counts_a_corrupted_spec_as_a_parse_mismatch():
    rows = _rows()
    for r in rows:
        if r["form"] == "AR-F1":
            r["spec"] = copy.deepcopy(r["spec"])
            r["spec"]["base"][0]["value"] = "999"       # the text says something else
    per_form, ans, parse, _ = H.run(rows)
    assert per_form["AR-F1"]["parse_mismatch"] == per_form["AR-F1"]["rows"]
    assert per_form["AR-F2"]["parse_mismatch"] == 0


def test_b_is_deterministic():
    rows = _rows(3)
    a = [H.solve_row({k: r[k] for k in ("form", "k", "carrier", "stem", "options")}) for r in rows]
    b = [H.solve_row({k: r[k] for k in ("form", "k", "carrier", "stem", "options")}) for r in rows]
    assert a == b


def test_b_agrees_with_a_on_a_fresh_seed():
    rows = H.build_rows("harness-fresh-seed", 12, "both")
    per_form, ans, parse, _ = H.run(rows)
    total = sum(c["rows"] for c in per_form.values())
    agree = sum(c["agree"] for c in per_form.values())
    assert agree == total          # the relation-fact negation render defect is fixed (skeptic 18 Oct): no disagreement is tolerated
    assert sum(c["parse_fail"] + c["reject"] for c in per_form.values()) == 0
