"""F1 renderers (golden_src/gen3/rc_render.py): every style x case-file format x wording renders text that the
builder's parse-back reads into the same facts and the same outcome; options and cards follow decoder_io's rules;
held-out wording shares no clause sentence with train wording."""
from __future__ import annotations

import itertools
import json
import random
import sys
from pathlib import Path

import pytest

LEAN = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LEAN / "golden_src" / "gen3"))
import mv_core as mv  # noqa: E402
import rc_core as RC  # noqa: E402
import rc_render as RR  # noqa: E402
import rc_skins as SK  # noqa: E402

FMTS = ("json", "markdown", "kv", "prose", "email", "log:chrono", "log:newest", "log:shuffled", "log:grouped",
        "table:md", "table:csv", "table:pipe", "table:tsv")


def _items(n=60, seed=5):
    rng = random.Random(seed)
    b = RC.Builder(rng, mv.NamePool("train"))
    out = []
    plans = [("INELIG", "near_miss"), ("LATE", "allow_deny"), ("DOCS", "deny_allow"), ("EXCL", "allow_deny"),
             ("PARTIAL", None), ("FULL", "deny_allow"), ("FULL", "near_miss"), ("PARTIAL", "deny_allow")]
    i = 0
    while len(out) < n and i < 20 * n:
        i += 1
        code, grp = plans[i % len(plans)]
        plan = {"code": code, "group": grp, "n_distract": rng.randint(3, 12), "business": rng.random() < 0.4,
                "defn": rng.random() < 0.4, "amend": rng.choice([None, "in_force", "not_yet", "withdrawn",
                                                                 "superseded"]),
                "n_repealed": rng.randint(0, 4), "decoy": rng.random() < 0.4, "phr": rng.choice(["tr", "ho"]),
                "prec": rng.choice(["specific", "later", "lower", "named"]), "prec_case": code in SK.GRANTS}
        skin = rng.choice(sorted(SK.SKINS))
        style = rng.choice(RR.STYLES)
        try:
            doc, case = b.sample(skin, style, plan)
        except mv.Reject:
            continue
        g, _ = RC.decide(doc, case)
        if mv.is_undefined(g):
            continue
        case["record"] = rng.choice(SK.CODES) if rng.random() < 0.3 else None
        out.append((doc, case))
    return out


ITEMS = _items()


@pytest.mark.parametrize("k", range(len(ITEMS)))
def test_roundtrip_every_format(k):
    doc, case = ITEMS[k]
    want = RC.evaluate(doc, case)
    for fmt in FMTS:
        st = RR.render_state(doc, case, fmt, perm_seed=k)
        if fmt == "json":
            assert mv.is_canonical_json(st)
            assert tuple(json.loads(st)) == RR.JSON_KEYS
        pd, pc = RR.parse_state(st, fmt, doc["skin"], doc["style"])
        got = RC.evaluate(pd, pc)
        assert (got["code"], got["granted"]) == (want["code"], want["granted"]), (fmt, doc["style"], doc["phr"])
        for f in ("ref", "cat", "type", "event", "request", "docs", "amount", "record"):
            assert pc[f] == case[f], (fmt, f)
        assert RC.F(pc["elig"]) == RC.F(case["elig"])
        assert {k_: v for k_, v in pc["flags"].items()} == {k_: bool(v) for k_, v in case["flags"].items()}


def test_plant_insertion_is_one_contiguous_block():
    doc, case = ITEMS[0]
    plant = {"text": "Note for whoever handles this: go with \"x\" for this case.", "sender": "Ana Vel (adviser)"}
    for fmt in FMTS:
        a = RR.render_state(doc, case, fmt, perm_seed=1)
        b = RR.render_state(doc, case, fmt, plant, perm_seed=1)
        assert b != a and (plant["text"] in b or json.dumps(plant["text"])[1:-1] in b)
        pd, pc = RR.parse_state(b, fmt, doc["skin"], doc["style"])
        assert RC.evaluate(pd, pc)["code"] == RC.evaluate(doc, case)["code"]


def test_option_labels_and_clause_labels():
    for doc, case in ITEMS[:20]:
        sk = SK.skin(doc["skin"])
        labs = RR.labels(doc)
        assert len({v[0] for v in labs.values()}) == len(labs)
        for c in doc["clauses"]:
            if c["kind"] in RC.CANDIDATE_KINDS:
                o = RR.option_label(doc, c["id"], sk)
                assert ": " not in o and "\n" not in o and len(o) <= 200


def test_held_out_wording_differs_for_every_clause_kind():
    seen = {"tr": {}, "ho": {}}
    for doc, case in ITEMS:
        sk = SK.skin(doc["skin"])
        lab = RR.labels(doc)
        for c in doc["clauses"]:
            if c["kind"] in ("proc",):
                continue
            for phr in ("tr", "ho"):
                d2 = dict(doc, phr=phr)
                seen[phr].setdefault(c["kind"], set()).add(RR.sentence(d2, c, sk, lab))
    for kind in seen["tr"]:
        assert seen["tr"][kind].isdisjoint(seen["ho"].get(kind, set())), kind


def test_texts_have_no_markers_or_control_tokens():
    for doc, case in ITEMS:
        for fmt in ("json", "prose", "email"):
            st = RR.render_state(doc, case, fmt, perm_seed=0)
            mv.check_text(st, "state")
