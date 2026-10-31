"""Wording-pool AUDIT (T54, T55, T56): the production pools (pools/wording_pool_v1.json) are the text every row is rendered from, and
solver B's text parser recognises wordings by exact match against them, so a pool defect is a label defect. These checks are
program-only and independent of the builders' round trip (which only compares slot sets, numbers and negation COUNTS): file sha vs
manifest, seed round trip re-run, ASCII/space hygiene, uniqueness within a form and across the option forms of one family, option
polarity (T56), error-phrase class separation (T55), and the lexicon round trip (every wording of every form is recognised by solver
B's lexicon as exactly its own form)."""
import json
import os
import re
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))          # .../c21_fam
for p in (ROOT, os.path.join(ROOT, "T54"), os.path.join(ROOT, "T55"), os.path.join(ROOT, "T56"),
          os.path.join(ROOT, "T54", "solver_b"), os.path.join(ROOT, "T55", "solver_b"), os.path.join(ROOT, "T56", "solver_b")):
    if p not in sys.path:
        sys.path.insert(0, p)

import t54_render_b  # noqa: E402
import t54_wording  # noqa: E402
import t55_render_b  # noqa: E402
import t55_wording  # noqa: E402
import t56_solver_b  # noqa: E402
import t56_wording  # noqa: E402
from tool_engine import wording as wd  # noqa: E402
from tool_engine import wording_expand as X  # noqa: E402

FAMS = {"T54": t54_wording, "T55": t55_wording, "T56": t56_wording}


def _load(fam):
    base = os.path.join(ROOT, fam, "pools")
    with open(os.path.join(base, "wording_pool_v1.json"), "r", encoding="utf-8") as f:
        pools = json.load(f)
    with open(os.path.join(base, "pool_manifest.json"), "r", encoding="utf-8") as f:
        manifest = json.load(f)
    return pools, manifest


@pytest.mark.parametrize("fam", sorted(FAMS))
def test_pool_matches_its_manifest_and_every_form_has_enough_wordings(fam):
    pools, man = _load(fam)
    assert X.pool_sha(pools) == man["pool_sha256"]
    assert man["forms"] == len(pools) and man["min_per_form"] == min(len(v) for v in pools.values()) >= 50
    assert all(man["per_form"][k]["count"] == len(v) for k, v in pools.items())
    seed = FAMS[fam].seed_pool().pools
    assert set(seed) == set(pools), set(seed) ^ set(pools)               # no form without a pool, no pool without a seed


@pytest.mark.parametrize("fam", sorted(FAMS))
def test_every_wording_passes_the_seed_round_trip_and_is_clean_text(fam):
    pools, _man = _load(fam)
    seed = FAMS[fam].seed_pool().pools
    for form, ws in pools.items():
        assert len(set(ws)) == len(ws), form                                # unique within the form
        for w in ws:
            assert wd.reword_ok(seed[form][0], w), (form, w)                # slots, numbers and negations as the seed
            assert w == w.strip() and "  " not in w and w.isascii() and "\n" not in w, (form, w)
            if form.startswith("phrase."):                                  # tool-output text: no second person (the output lint's rule)
                assert not re.search(r"\b(?:you|your|yours|we|our)\b", w, re.I), (form, w)


@pytest.mark.parametrize("fam", sorted(FAMS))
def test_option_wordings_never_repeat_across_the_label_forms_of_a_family(fam):
    pools, _man = _load(fam)
    seen = {}
    for form, ws in pools.items():
        if not form.startswith("opt."):
            continue
        for w in ws:
            assert w not in seen, (w, form, seen.get(w))
            seen[w] = form


def test_t56_option_polarity():
    pools, _man = _load("T56")
    neg = r"\b(no|not|n't|never|more work|unfinished|go on|keep working|continue|must not|incomplete|remain|stays?|hold)\b"
    for lab in ("DONE", "CONTINUE", "READY", "NOT_READY"):
        isneg = lab in ("CONTINUE", "NOT_READY")
        for w in pools["opt." + lab]:
            assert bool(re.search(neg, w, re.I)) == isneg, (lab, w)


def test_t55_error_phrases_do_not_straddle_two_classes():
    pools, _man = _load("T55")
    own = {"rate": r"rate|too many|volume|traffic|window|ceiling|excess|burst|throttl|calls|count",
           "quota": r"quota|allowance|budget|used up|spent|consumed|exhaust|period",
           "temp": r"temporar|unavailab|slow|unresponsive|down|busy|starting|timed out|not ready|for now|moment",
           "auth": r"credential|token|key|session|sign-in|authoris|access|caller|permission|allowed|permitted|honou?red|recognis|accepted|grant|authentication",
           "arg": r"argument|value|field|parameter|format|parse|validation|malformed|invalid|payload",
           "unsup": r"support|implement|handler|cannot be carried|sort of operation|offer|expose|cover|route|cannot run|cannot be run|does not handle|does not accept|available",
           "fatal": r"no longer|permanently|deleted|removed|cannot be (met|completed|reached)|unreachable|gone|not in scope|not part of|reachable"}
    # the two classes that share vocabulary in a quota / rate pair must keep their own words apart
    for g in ("rate", "quota"):
        other = "quota" if g == "rate" else "rate"
        banned = r"budget|quota|allowance|period|used up|spent|consumed|exhaust" if g == "rate" else r"window|ceiling|per-window|rate|too many|cap\b|traffic|volume"
        for w in pools["phrase." + g]:
            assert re.search(own[g], w, re.I), (g, w)
            assert not re.search(banned, w, re.I), (g, other, w)
    for g, pat in own.items():
        for w in pools["phrase." + g]:
            assert re.search(pat, w, re.I), (g, w)


def test_lexicon_round_trip_every_wording_is_recognised_as_its_own_form():
    pools, _ = _load("T54")
    t54_render_b.set_lexicon(pools)
    try:
        for lab in ("CALL", "ASK", "NO_TOOL", "ANSWER", "RESULT_MISSING", "WRITE", "READ_FIRST", "DONE_NO_CALL", "GROUNDED", "UNGROUNDED"):
            for w in pools["opt." + lab]:
                assert t54_render_b.classify_option(w) == lab, (lab, w)
        for cid, flag in (("card.card.t54.defaults_ok", True), ("card.card.t54.strict_ask", False)):
            for w in pools[cid]:
                assert t54_render_b.card_flags(w) is flag, (cid, w)
    finally:
        t54_render_b.set_lexicon({})
    pools, _ = _load("T55")
    t55_render_b.set_lexicon(pools)
    try:
        fam_labels = t55_render_b._FAM_LABELS
        for fam_, labs in fam_labels.items():
            for lab in labs:
                for w in pools["opt." + lab]:
                    assert t55_render_b.classify_option(w, fam_) == lab, (fam_, lab, w)
    finally:
        t55_render_b.set_lexicon({})
    pools, _ = _load("T56")
    t56_solver_b.set_lexicon(pools)
    try:
        for lab in ("DONE", "CONTINUE", "READY", "NOT_READY"):
            qk = "ready" if lab in ("READY", "NOT_READY") else "done"
            for w in pools["opt." + lab]:
                assert t56_solver_b.option_label(w, qk) == lab, (lab, w)
        for w in pools["q.ready"]:
            assert t56_solver_b.lex_find(["q.ready", "q.done"], w)[0] == "q.ready", w
        for w in pools["q.done"]:
            assert t56_solver_b.lex_find(["q.ready", "q.done"], w)[0] == "q.done", w
    finally:
        t56_solver_b.set_lexicon({})
