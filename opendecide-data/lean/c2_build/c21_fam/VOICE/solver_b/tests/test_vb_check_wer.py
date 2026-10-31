"""Span-survival checker and WER fixtures, worked out by hand from VOICE/SCHEMA.md sections 3 and 4."""
import pytest

import vb_check as BC
import vb_wer as BW


def word_doc(words, spans, numbers=()):
    """A document whose tokens are all words, except the (start, end, style) ranges in `numbers` which are number segments."""
    segs = []
    i = 0
    src = 0
    num_at = dict((a, (b, st)) for a, b, st in numbers)
    while i < len(words):
        if i in num_at:
            b, st = num_at[i]
            segs.append({"kind": "number", "tok": [i, b], "src": src, "style": st})
            i = b
        else:
            segs.append({"kind": "word", "tok": [i, i + 1], "src": src, "style": "word"})
            i += 1
        src += 1
    return {"tokens": list(words), "segments": segs, "spans": spans, "stratum": "V-NL"}


PORT_DOC = word_doc(["do", "not", "run", "the", "build", "on", "port", "four", "hundred", "forty", "three"],
                    [{"id": 0, "role": "negation", "kind": "negation", "canonical": "not", "tok": [1, 2], "partial": False, "fallback": False},
                     {"id": 1, "role": "number", "kind": "number", "canonical": "443", "tok": [7, 11], "partial": False, "fallback": False}],
                    numbers=[(7, 11, "cardinal")])


@pytest.mark.parametrize("hyp,kept", [
    ("Do not run the build on port 443.", True),
    ("Do not run the build on port four four three.", True),
    ("Do not run build on port four hundred and forty three", True),
    ("don't run the build on port 443", True),
    ("Do not um run the build on port 443", True),
    ("Do run the build on port 443.", False),
    ("Do not run the build on port 444.", False),
    ("Do not run the build on port 4430", False),
    ("Do not run the build on port.", False),
    ("Do not not run the build on port 443", False),
    ("Do not run the build on port one hundred", False),
])
def test_negation_and_number_spans(hyp, kept):
    assert BC.check(PORT_DOC, hyp) is kept


FILE_DOC = {"tokens": ["delete", "the", "file", "tee", "em", "pee", "dot", "log"],
            "segments": [{"kind": "word", "tok": [0, 1], "src": 0, "style": "word"}, {"kind": "word", "tok": [1, 2], "src": 1, "style": "word"},
                         {"kind": "word", "tok": [2, 3], "src": 2, "style": "word"}, {"kind": "spelled", "tok": [3, 6], "src": 3, "style": "letters"},
                         {"kind": "sym", "tok": [6, 7], "src": 3, "style": "sym"}, {"kind": "word", "tok": [7, 8], "src": 3, "style": "word"}],
            "spans": [{"id": 0, "role": "entity", "kind": "path", "canonical": "tmp.log", "tok": [3, 8], "partial": False, "fallback": False}],
            "stratum": "V-DICT-LIT"}


@pytest.mark.parametrize("hyp,kept", [
    ("Delete the file tmp.log", True),
    ("delete the file t m p dot log", True),
    ("delete the file tmp dot log", True),
    ("delete the file TMP.LOG.", True),
    ("delete the file tee em pee dot log", True),
    ("delete the file tmp.lock", False),
    ("delete the file tmp", False),
    ("delete the file temp.log", False),
    ("delete the file xtmp.log", False),
    ("delete the file", False),
])
def test_entity_span(hyp, kept):
    assert BC.check(FILE_DOC, hyp) is kept


DATE_DOC = word_doc(["before", "june", "fifth", "twenty", "twenty", "six"],
                    [{"id": 0, "role": "number", "kind": "date", "canonical": "2026-06-05", "tok": [1, 6], "partial": False, "fallback": False}],
                    numbers=[(1, 6, "date")])


@pytest.mark.parametrize("hyp,kept", [
    ("before June 5th 2026", True), ("before 2026-06-05", True), ("before 5 June 2026", True), ("before june fifth twenty twenty six", True),
    ("before June 6th 2026", False), ("before June 5th 2027", False), ("before June", False),
])
def test_date_span(hyp, kept):
    assert BC.check(DATE_DOC, hyp) is kept


def test_the_same_number_is_not_counted_twice():
    doc = word_doc(["ports", "eighty", "and", "eighty"],
                   [{"id": 0, "role": "number", "kind": "number", "canonical": "80", "tok": [1, 2], "partial": False, "fallback": False},
                    {"id": 1, "role": "number", "kind": "number", "canonical": "80", "tok": [3, 4], "partial": False, "fallback": False}],
                   numbers=[(1, 2, "cardinal"), (3, 4, "cardinal")])
    assert BC.check(doc, "ports 80 and 80") is True
    assert BC.check(doc, "ports 80 and") is False


def test_a_no_inside_a_flag_is_not_a_negation():
    doc = {"tokens": ["run", "with", "dash", "dash", "no", "dash", "verify"],
           "segments": [{"kind": "word", "tok": [0, 1], "src": 0, "style": "word"}, {"kind": "word", "tok": [1, 2], "src": 1, "style": "word"},
                        {"kind": "sym", "tok": [2, 3], "src": 2, "style": "sym"}, {"kind": "sym", "tok": [3, 4], "src": 2, "style": "sym"},
                        {"kind": "word", "tok": [4, 5], "src": 2, "style": "word"}, {"kind": "sym", "tok": [5, 6], "src": 2, "style": "sym"},
                        {"kind": "word", "tok": [6, 7], "src": 2, "style": "word"}],
           "spans": [{"id": 0, "role": "entity", "kind": "flag", "canonical": "--no-verify", "tok": [2, 7], "partial": False, "fallback": False}],
           "stratum": "V-DICT-LIT"}
    assert BC.check(doc, "run with --no-verify") is True
    assert BC.check(doc, "run with dash dash no dash verify") is True
    assert BC.check(doc, "run with --verify") is False


def test_context_recoverable_exception_is_off():
    assert BC.CTX_RECOVERABLE_ENABLED is False
    # the number appears elsewhere in the row, but the spoken span itself is gone: still dropped
    assert BC.check(PORT_DOC, "Do not run the build on port 8080 and 443") is True   # the value is present
    assert BC.check(PORT_DOC, "Do not run the build on port eight zero eight zero") is False


# ---- WER ----
WORDS = word_doc(["a", "b", "c", "d"], [])


@pytest.mark.parametrize("hyp,want", [("a b c d", 0.0), ("a b x d", 0.25), ("a c d", 0.25), ("a b b c d", 0.25), ("a b c d um", 0.0), ("", 1.0)])
def test_plain_word_wer(hyp, want):
    assert BW.wer(WORDS, hyp) == pytest.approx(want)


def test_written_forms_match_spoken_runs():
    toks = ["open", "slash", "tee", "em", "pee", "slash", "bee", "port", "eight", "zero", "eight", "zero"]
    segs = [{"kind": "word", "tok": [0, 1], "src": 0, "style": "word"},
            {"kind": "sym", "tok": [1, 2], "src": 1, "style": "sym"}, {"kind": "spelled", "tok": [2, 5], "src": 1, "style": "letters"},
            {"kind": "sym", "tok": [5, 6], "src": 1, "style": "sym"}, {"kind": "spelled", "tok": [6, 7], "src": 1, "style": "letters"},
            {"kind": "word", "tok": [7, 8], "src": 2, "style": "word"}, {"kind": "number", "tok": [8, 12], "src": 3, "style": "digits"}]
    doc = {"tokens": toks, "segments": segs, "spans": [], "stratum": "V-NL"}
    assert BW.wer(doc, "open /tmp/b port 8080") == 0.0
    assert BW.wer(doc, "open slash tmp slash b port eight zero eight zero") == 0.0
    assert BW.wer(doc, "open /tmp/b port 8081", fine=False) == pytest.approx(0.25)


def test_fine_token_and_whitespace_token_readings_differ_for_a_wrong_date():
    doc = word_doc(["x", "june", "fifth", "twenty", "twenty", "six"],
                   [], numbers=[(1, 6, "date")])
    assert BW.wer_detail(doc, "x 2026-06-06", fine=False)["errors"] == 1
    assert BW.wer_detail(doc, "x 2026-06-06", fine=True)["errors"] == 5     # '2026', '-', '06', '-', '06' are five tokens


@pytest.mark.parametrize("w,band", [(0.0, 0), (0.029, 0), (0.03, 1), (0.079, 1), (0.08, 2), (0.149, 2), (0.15, 3), (0.249, 3), (0.25, None), (1.2, None)])
def test_bands(w, band):
    assert BW.band_of(w) == band


def test_two_numbers_made_adjacent_by_a_dropped_word_still_survive():
    doc = word_doc(["port", "eighty", "in", "four", "hundred", "seventy", "one", "hours"],
                   [{"id": 0, "role": "number", "kind": "number", "canonical": "80", "tok": [1, 2], "partial": False, "fallback": False},
                    {"id": 1, "role": "number", "kind": "number", "canonical": "471", "tok": [3, 7], "partial": False, "fallback": False}],
                   numbers=[(1, 2, "cardinal"), (3, 7, "cardinal")])
    assert BC.check(doc, "port eighty four hundred seventy one hours") is True          # 'in' dropped: the two numbers touch
    assert BC.check(doc, "port eighty four hundred seventy two hours") is False         # a changed digit is still caught
    assert BC.check(doc, "port 80 in 471 hours") is True


def test_a_spelled_letter_o_next_to_a_number_word_is_not_a_zero():
    doc = word_doc(["serbeso", "in", "three", "hundred", "thirty", "four"],
                   [{"id": 0, "role": "number", "kind": "number", "canonical": "334", "tok": [2, 6], "partial": False, "fallback": False}],
                   numbers=[(2, 6, "cardinal")])
    assert BC.check(doc, "s e r b e s o three hundred thirty four") is True
