import random
import unicodedata

import pytest

from LA_COMMON import perturb as P
from LA_COMMON.canon import rng_for
from LA_COMMON.spans import ROLE_AUTHORITY, ROLE_ENTITY, ROLE_NEGATION, ROLE_NUMBER, make_span

SENT = "Please do not delete the build cache, and only remove the old files from the folder; don't touch the rest."

NEG = ["not", "never", "don't", "no", "without", "cannot"]
AUTH = ["you may remove the cache folder", "only the old files", "I approve deleting the logs", "go ahead and clean up",
        "leave everything else alone"]
ENT = ["/srv/ab/cd", "--force", "main", "origin", "feature-x", "pkg.tar.gz", "https://x.example/a?b=1", "$HOME", "rm"]
NUM = ["3", "12", "three", "500", "v2"]
PLAIN = ("please run the cleanup on the staging folder before we ship because the report looks fine and the team asked "
         "about it today so just handle the old branches carefully with that tool").split()


def make_row(seed):
    """-> (text, spans, protect). Synthetic sentence with exact-offset spans of the four roles."""
    r = random.Random(seed)
    parts = []
    for _ in range(r.randint(5, 9)):
        k = r.random()
        if k < 0.35:
            parts.append(("plain", " ".join(r.choice(PLAIN) for _ in range(r.randint(1, 3)))))
        elif k < 0.55:
            parts.append(("neg", r.choice(NEG)))
        elif k < 0.70:
            parts.append(("auth", r.choice(AUTH)))
        elif k < 0.85:
            parts.append(("ent", r.choice(ENT)))
        else:
            parts.append(("num", r.choice(NUM)))
    text, spans, pos = "", [], 0
    roles = {"neg": [ROLE_NEGATION], "auth": [ROLE_AUTHORITY], "ent": [ROLE_ENTITY], "num": [ROLE_NUMBER]}
    for kind, piece in parts:
        if text:
            text += " "
        start = len(text)
        text += piece
        if kind in roles:
            spans.append(make_span(0, kind, start, len(text), roles[kind]))
    text += "."
    protect = [(s["start"], s["end"]) for s in spans if set(s["roles"]) & {ROLE_ENTITY, ROLE_NUMBER}]
    return text, spans, protect


def ids_and_rngs(tid, tag, n=1):
    return [rng_for("t", tid, tag, i) for i in range(n)]


def test_ids_are_the_canonical_gv6_ids_and_held_out_never_trained():
    assert P.TRAINED_TRANSFORMS == ("pert.diacritics", "pert.spacing", "pert.leetspeak", "pert.homoglyph", "pert.zero_width")
    assert P.HELDOUT_TRANSFORMS == ("pert.fullwidth", "pert.bidi", "pert.upside_down")
    assert not set(P.TRAINED_TRANSFORMS) & set(P.HELDOUT_TRANSFORMS)
    assert set(P.ALL_TRANSFORMS) == set(P.TRAINED_TRANSFORMS) | set(P.HELDOUT_TRANSFORMS) and len(P.ALL_TRANSFORMS) == 8
    assert P.trained_choices() == P.TRAINED_TRANSFORMS
    assert P.trained_choices(removed=["pert.spacing"]) == tuple(t for t in P.TRAINED_TRANSFORMS if t != "pert.spacing")
    drawn = {P.choose_trained(random.Random(i)) for i in range(400)}
    assert drawn == set(P.TRAINED_TRANSFORMS) and not drawn & set(P.HELDOUT_TRANSFORMS)
    with pytest.raises(ValueError):
        P.choose_trained(random.Random(0), removed=P.TRAINED_TRANSFORMS)
    with pytest.raises(ValueError):
        P.apply("pert.nope", SENT, random.Random(0))


@pytest.mark.parametrize("tid", P.ALL_TRANSFORMS)
def test_each_transform_changes_text_is_deterministic_and_has_a_valid_map(tid):
    out = []
    for seed in range(8):
        new, omap = P.apply(tid, SENT, rng_for("d", tid, seed))
        assert new != SENT and P.check_offset_map(omap, len(SENT), len(new))
        again, omap2 = P.apply(tid, SENT, rng_for("d", tid, seed))
        assert (new, omap) == (again, omap2)                              # deterministic given the rng
        out.append(new)
    assert len(set(out)) > 1                                                # the seed matters
    new, _ = P.apply(tid, "", rng_for("e"))
    assert new == ""
    new, omap = P.apply(tid, "12345 /srv/a/b --force", rng_for("e"))      # nothing perturbable: unchanged, identity map
    assert new == "12345 /srv/a/b --force" and P.check_offset_map(omap, len(new), len(new))


@pytest.mark.parametrize("tid", P.ALL_TRANSFORMS)
def test_protected_ranges_stay_byte_identical_and_map_exactly(tid):
    for seed in range(40):
        text, spans, protect = make_row(seed)
        # also protect a plain word (letters only) explicitly
        first = text.split(" ")[0]
        protect = protect + [(0, len(first))]
        new, omap = P.apply(tid, text, rng_for("p", tid, seed), protect=protect)
        for s, e in protect:
            ns, ne = P.map_range(omap, s, e)
            assert new[ns:ne] == text[s:e]
        assert new[:len(first)] == first


def test_zero_width_inserts_only_u200b_inside_words():
    for seed in range(60):
        text, _, protect = make_row(seed)
        new, omap = P.apply("pert.zero_width", text, rng_for("z", seed), protect=protect)
        assert set(new) - set(text) <= {"\u200b"}
        assert new.replace("\u200b", "") == text
        for i, ch in enumerate(new):
            if ch == "\u200b":                                             # between two letters, never at an edge
                assert new[i - 1].isalpha() and new[i + 1].isalpha() and "\u200b" not in (new[i - 1], new[i + 1])
    new, _ = P.apply("pert.zero_width", SENT, rng_for("z"))
    assert "\u200b" in new and not P.forbidden_codepoints(new)


@pytest.mark.parametrize("tid", P.ALL_TRANSFORMS)
def test_no_forbidden_code_points_ever(tid):
    for seed in range(120):
        text, _, protect = make_row(seed)
        new, _ = P.apply(tid, text, rng_for("f", tid, seed), protect=protect)
        assert P.forbidden_codepoints(new) == []
        for ch in new:
            cp = ord(ch)
            assert cp not in (0x200C, 0x200D) and not 0xE0000 <= cp <= 0xE007F and not 0xFE00 <= cp <= 0xFE0F
            assert not 0xE0100 <= cp <= 0xE01EF
    for bad in ("a\u200db", "a\u200cb", "a\U000e0041b", "a\ufe0fb", "a\U000e0100b"):
        assert P.forbidden_codepoints(bad)
        with pytest.raises(ValueError):
            P.apply(tid, bad + " word", random.Random(1))


def test_only_natural_language_words_are_touched():
    tricky = ("run `git push origin main` then see /srv/app/tmp --force -rf KEY=value https://x.example/a.b?c=1 "
              "snake_case CamelCase SHOUT 123 v2 foo.txt a/b $HOME ~/x user@host.example 3.5 e.g. i.e.")
    for tid in P.ALL_TRANSFORMS:
        new, _ = P.apply(tid, tricky, rng_for("w", tid))
        # the only words that may change are 'run', 'then', 'see'
        assert new.split("`")[1:2] == ["git push origin main"]
        for tok in tricky.split()[7:]:
            assert tok in new.replace("\u200b", ""), (tid, tok)
    # a command token and the rest of its sentence are never touched; the next sentence is
    text = "Run git push origin main now. Please delete the cache"
    for tid in P.ALL_TRANSFORMS:
        new, _ = P.apply(tid, text, rng_for("c", tid))
        assert "git push origin main now." in new
    # prompt lines and backtick spans
    block = "$ cat notes about things\nplease delete the cache"
    for tid in P.ALL_TRANSFORMS:
        new, _ = P.apply(tid, block, rng_for("b", tid))
        assert new.startswith("$ cat notes about things\n")


@pytest.mark.parametrize("tid", P.ALL_TRANSFORMS)
def test_spans_round_trip_for_200_random_sentences(tid):
    changed = 0
    for seed in range(200):
        text, spans, protect = make_row(seed)
        new, omap = P.apply(tid, text, rng_for("rt", tid, seed), protect=protect)
        changed += new != text
        assert P.check_offset_map(omap, len(text), len(new))
        new_spans = P.remap_spans(spans, omap)
        assert [(s["turn"], s["slot"], s["roles"]) for s in new_spans] == [(s["turn"], s["slot"], s["roles"]) for s in spans]
        for o, n in zip(spans, new_spans):
            assert 0 <= n["start"] < n["end"] <= len(new)
            if set(o["roles"]) & {ROLE_ENTITY, ROLE_NUMBER}:
                assert new[n["start"]:n["end"]] == text[o["start"]:o["end"]]
        ok, reasons = P.spans_survive(text, spans, new, new_spans)
        assert ok, (tid, seed, text, new, reasons)
    assert changed >= 150                                                  # the transform really perturbs most rows


def test_span_order_and_gaps_are_preserved_by_the_remap():
    for tid in P.ALL_TRANSFORMS:
        text, spans, protect = make_row(7)
        new, omap = P.apply(tid, text, rng_for("o", tid), protect=protect)
        ns = P.remap_spans(spans, omap)
        ends = [(s["start"], s["end"]) for s in ns]
        assert ends == sorted(ends) and all(a[1] <= b[0] for a, b in zip(ends, ends[1:]))


def test_chained_transforms_turn_scoped_remap_and_multi_turn_texts():
    text, spans, protect = make_row(11)
    a, m1 = P.apply("pert.zero_width", text, rng_for("c1"), protect=protect)
    protect2 = [P.map_range(m1, s_, e_) for s_, e_ in protect]
    b, m2 = P.apply("pert.diacritics", a, rng_for("c2"), protect=protect2)
    chained = P.remap_spans(P.remap_spans(spans, m1), m2)               # successive remaps are exact
    ok, reasons = P.spans_survive(text, spans, b, chained)
    assert ok, reasons
    # turn scoping: other turns' spans are copied unchanged
    other = [make_span(1, "s", 0, 2, [ROLE_NEGATION])] + spans
    out = P.remap_spans(other, m1, turn=0)
    assert out[0] == other[0] and out[1:] == P.remap_spans(spans, m1)
    # multi-turn texts: list of {'text': ...} or plain strings or a dict keyed by turn
    t0, t1 = "history text", "Please do not delete it."
    s1 = [make_span(1, "neg", 10, 13, [ROLE_NEGATION])]
    n1, m = P.apply("pert.homoglyph", t1, rng_for("mt"))
    ns1 = P.remap_spans(s1, m, turn=1)
    for orig, new in (([{"text": t0}, {"text": t1}], [{"text": t0}, {"text": n1}]), ([t0, t1], [t0, n1]), ({1: t1}, {1: n1})):
        assert P.spans_survive(orig, s1, new, ns1) == (True, [])


def test_spans_survive_accepts_normal_perturbations_of_authority_and_negation():
    text = "You may remove only the old cache, do not delete the rest."
    spans = [make_span(0, "auth", 0, 33, [ROLE_AUTHORITY]), make_span(0, "neg", 35, 41, [ROLE_NEGATION])]
    assert text[0:33] == "You may remove only the old cache" and text[35:41] == "do not"
    for tid in P.ALL_TRANSFORMS:
        for seed in range(15):
            new, omap = P.apply(tid, text, rng_for("a", tid, seed))
            ok, reasons = P.spans_survive(text, spans, new, P.remap_spans(spans, omap))
            assert ok, (tid, new, reasons)


def test_spans_survive_rejects_broken_cases():
    text = "You may remove only 3 files from /srv/a/b but do not touch main"
    def span(slot, sub, role):
        i = text.index(sub)
        return make_span(0, slot, i, i + len(sub), [role])
    spans = [span("auth", "You may remove only", ROLE_AUTHORITY), span("num", "3", ROLE_NUMBER),
             span("path", "/srv/a/b", ROLE_ENTITY), span("neg", "do not", ROLE_NEGATION)]
    ident = [dict(s) for s in spans]
    assert P.spans_survive(text, spans, text, ident) == (True, [])

    # 1. a transform applied inside an AUTHORITY span with NO normalisation mapping (confusable outside the tables)
    broken = text.replace("remove", "rem\u0585ve")                      # Armenian oh: looks like o, not in any map
    ok, reasons = P.spans_survive(text, spans, broken, ident)
    assert not ok and any("AUTHORITY" in r for r in reasons)
    # a letter swap that changes the word is not a perturbation either
    ok, reasons = P.spans_survive(text, spans, text.replace("remove", "rename"), ident)
    assert not ok
    # the SAME confusable is fine when it is in the homoglyph table
    ok, _ = P.spans_survive(text, spans, text.replace("remove", "rem\u043eve"), ident)
    assert ok

    # 2. a changed number
    for bad in ("30", "2", "three", "3\u200b"):
        new = text.replace(" 3 ", " %s " % bad)
        shift = len(bad) - 1
        sp = [dict(s) for s in ident]
        sp[1]["end"] += shift
        sp[2] = dict(sp[2], start=sp[2]["start"] + shift, end=sp[2]["end"] + shift)
        sp[3] = dict(sp[3], start=sp[3]["start"] + shift, end=sp[3]["end"] + shift)
        ok, reasons = P.spans_survive(text, spans, new, sp)
        assert not ok and any("number" in r for r in reasons), (bad, reasons)

    # 3. entity changed by one character / homoglyphed entity / zero-width inside the path
    for bad in ("/srv/a/c", "/srv/\u0430/b", "/srv/a\u200b/b"):
        new = text.replace("/srv/a/b", bad)
        sp = [dict(s) for s in ident]
        sp[2]["end"] = sp[2]["start"] + len(bad)
        sp[3] = dict(sp[3], start=sp[3]["start"] + len(bad) - 8, end=sp[3]["end"] + len(bad) - 8)
        ok, reasons = P.spans_survive(text, spans, new, sp)
        assert not ok and any("entity/path/flag" in r for r in reasons), (bad, reasons)

    # 4. negation lost or changed, offsets that do not index the text, span lists that differ
    new = text.replace("do not", "do now")
    assert not P.spans_survive(text, spans, new, ident)[0]
    sp = [dict(s) for s in ident]
    sp[0]["end"] = len(text) + 5
    ok, reasons = P.spans_survive(text, spans, text, sp)
    assert not ok and any("index" in r for r in reasons)
    assert not P.spans_survive(text, spans, text, ident[:-1])[0]
    sp = [dict(s) for s in ident]
    sp[0]["roles"] = [ROLE_NEGATION]
    assert not P.spans_survive(text, spans, text, sp)[0]

    # 5. a held-out style transform applied but the offsets NOT remapped: the spans no longer land on the words
    new, omap = P.apply("pert.spacing", text, rng_for("rj"), protect=[(s["start"], s["end"]) for s in spans[1:3]])
    assert new != text
    ok, _ = P.spans_survive(text, spans, new, P.remap_spans(spans, omap))
    assert ok
    ok, _ = P.spans_survive(text, spans, new, ident)                      # stale offsets: rejected, nothing repaired
    assert not ok


def test_normalisation_does_not_make_different_words_equal():
    for a, b in (("delete", "remove"), ("do not", "do"), ("never", "ever"), ("approve", "approved"), ("only", "also")):
        assert not P.normalised_equal(a, b)
    for tid in P.ALL_TRANSFORMS:
        for seed in range(10):
            new, _ = P.apply(tid, "do not delete the cache", rng_for("n", tid, seed))
            assert P.normalised_equal("do not delete the cache", new)
            assert not P.normalised_equal("do delete the cache", new)


def test_k28_drop_rate_rule_removes_a_family_above_25_percent_only():
    res = ([("pert.spacing", True)] * 75 + [("pert.spacing", False)] * 25 +             # exactly 25%: kept
           [("pert.bidi", True)] * 70 + [("pert.bidi", False)] * 30 +                   # 30%: removed
           [("pert.leetspeak", True)] * 40)
    st = P.transform_survival_stats(res)
    assert st["per_transform"]["pert.spacing"] == {"n": 100, "dropped": 25, "drop_rate": 0.25}
    assert st["per_transform"]["pert.bidi"]["drop_rate"] == 0.3 and st["per_transform"]["pert.leetspeak"]["dropped"] == 0
    assert st["removed"] == ["pert.bidi"] and st["limit"] == 0.25
    assert P.transform_survival_stats([])["removed"] == []


@pytest.mark.parametrize("tid", P.ALL_TRANSFORMS)
def test_real_drop_rate_is_far_below_the_k28_limit(tid):
    results = []
    for seed in range(200):
        text, spans, protect = make_row(1000 + seed)
        new, omap = P.apply(tid, text, rng_for("k", tid, seed), protect=protect)
        ok, _ = P.spans_survive(text, spans, new, P.remap_spans(spans, omap))
        results.append((tid, ok))
    assert P.transform_survival_stats(results)["removed"] == []
    assert sum(not ok for _, ok in results) == 0


def test_tables_are_self_consistent():
    for base, opts in P.DIACRITICS.items():
        for g in opts:
            assert unicodedata.normalize("NFKD", g)[0] == base and len(g) == 1
    assert all(len(v) == 1 for v in P.LEET.values()) and set(P.LEET_INV) == set(P.LEET.values())
    for g, base in P.HOMOGLYPH_INV.items():
        assert base in P.HOMOGLYPHS and ord(g) > 127 and unicodedata.normalize("NFKD", g) == g
    assert len(P.FLIP_INV) == len(P.FLIP)
    assert all(unicodedata.normalize("NFKD", v) == k for k, v in P.FULLWIDTH.items())
    assert "\u200d" not in "".join(P.HOMOGLYPH_INV) and "\u200c" not in P.ZERO_WIDTH_SPACE
