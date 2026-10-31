"""Denormaliser fixtures worked out by hand from VOICE/SCHEMA.md section 2 (not copied from solver A)."""
import pytest

from vb_denorm import denormalise, invert_segment, DenormError, written_reference_words

CASES = [
    ("word", "word", ["please"], "please"),
    ("word", "hyphen", ["well", "known"], "well-known"),
    ("spelled", "letters", ["bee", "you", "eye", "el", "dee"], "build"),
    ("spelled", "letters", ["capital", "are", "eff"], "rf"),
    ("spelled", "letters_oov", ["double", "you", "ay", "why"], "way"),
    ("digits", "digits", ["four", "four", "three"], "443"),
    ("sym", "sym", ["slash"], "/"),
    ("sym", "sym", ["less", "than"], "<"),
    ("sym", "sym", ["open", "paren"], "("),
    ("sym", "sym", ["question", "mark"], "?"),
    ("number", "cardinal", ["two", "thousand", "twenty", "six"], "2026"),
    ("number", "cardinal", ["ninety", "nine"], "99"),
    ("number", "digits", ["two", "zero", "two", "six"], "2026"),
    ("number", "year", ["twenty", "twenty", "six"], "2026"),
    ("number", "year", ["nineteen", "oh", "five"], "1905"),
    ("number", "year", ["eleven", "hundred"], "1100"),
    ("number", "year", ["two", "thousand", "five"], "2005"),
    ("number", "year", ["nineteen", "ninety", "nine"], "1999"),
    ("number", "decimal", ["fifty", "eight", "point", "five"], "58.5"),
    ("number", "decimal", ["forty", "four", "point", "nine", "zero"], "44.90"),
    ("number", "cardinal_frac", ["three", "point", "twenty", "five"], "3.25"),
    ("number", "cardinal_frac", ["sixty", "four", "point", "ninety"], "64.90"),
    ("number", "version", ["two", "point", "twenty", "two", "point", "two"], "2.22.2"),
    ("number", "ordinal", ["thirty", "seventh"], "37th"),
    ("number", "ordinal", ["twelfth"], "12th"),
    ("number", "ordinal", ["first"], "1st"),
    ("number", "ordinal", ["twenty", "second"], "22nd"),
    ("number", "date", ["july", "tenth", "nineteen", "forty", "two"], "1942-07-10"),
    ("number", "date", ["may", "second", "twenty", "seventy", "two"], "2072-05-02"),
    ("number", "comma_cardinal", ["one", "thousand", "two", "hundred", "fifty", "three"], "1,253"),
    ("number", "comma_digits", ["one", "zero", "eight", "five"], "1,085"),
    ("number", "comma_year", ["fourteen", "fifty", "one"], "1,451"),
    ("number", "pct_cardinal", ["fifty", "one", "percent"], "51%"),
    ("number", "pct_digits", ["nine", "five", "percent"], "95%"),
    ("number", "neg_cardinal", ["minus", "forty", "three"], "-43"),
    ("number", "neg_digits", ["minus", "one", "three"], "-13"),
]


@pytest.mark.parametrize("kind,style,words,want", CASES)
def test_segment_inversion(kind, style, words, want):
    assert invert_segment(kind, style, words) == want


def test_one_source_token_with_several_segments_is_concatenated_and_disfluency_dropped():
    toks = ["um", "slash", "tee", "em", "pee", "slash", "bee", "now"]
    segs = [{"kind": "disfl", "tok": [0, 1], "src": None, "style": "disfl"},
            {"kind": "sym", "tok": [1, 2], "src": 0, "style": "sym"}, {"kind": "spelled", "tok": [2, 5], "src": 0, "style": "letters"},
            {"kind": "sym", "tok": [5, 6], "src": 0, "style": "sym"}, {"kind": "spelled", "tok": [6, 7], "src": 0, "style": "letters"},
            {"kind": "word", "tok": [7, 8], "src": 1, "style": "word"}]
    assert denormalise({"tokens": toks, "segments": segs, "stratum": "V-NL"}) == ["/tmp/b", "now"]


def test_written_reference_keeps_non_filler_disfluency_words_and_drops_fillers():
    toks = ["um", "the", "the", "build"]
    segs = [{"kind": "disfl", "tok": [0, 1], "src": None, "style": "disfl"}, {"kind": "disfl", "tok": [1, 2], "src": None, "style": "disfl"},
            {"kind": "word", "tok": [2, 3], "src": 0, "style": "word"}, {"kind": "word", "tok": [3, 4], "src": 1, "style": "word"}]
    assert written_reference_words({"tokens": toks, "segments": segs}) == ["the", "the", "build"]


def test_unreadable_segment_raises_not_guesses():
    with pytest.raises(DenormError):
        invert_segment("spelled", "letters", ["banana"])
    with pytest.raises(DenormError):
        invert_segment("number", "cardinal", ["banana"])
    with pytest.raises(DenormError):
        invert_segment("number", "date", ["july", "tenth"])
