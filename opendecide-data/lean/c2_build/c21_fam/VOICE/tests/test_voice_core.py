"""VOICE lane unit tests (CPU only). No audio, no TTS, no ASR, no model, no network; no file writes outside pytest tmp dirs."""
import random

import pytest

import disfluency as DF
import numwords as NW
import oracle_denorm as OD
import planted as PT
import span_check as SC
import verbalizer as VB
import vcommon as V
import wer as W

LEX = V.test_lexicon()
VBZ = VB.Verbalizer(LEX)


def rng(k=0):
    return random.Random("vt-%s" % k)


# ------------------------------------------------------------------ allow-list
def test_voice_allow_list_loads_and_refuses_off_list():
    a = V.VoiceAllow()
    assert a.carriers == frozenset(V.STRATA) and len(a.voices) == 15 and "am_adam" not in a.voices
    with pytest.raises(V.VoiceAllowError):
        a.check_voice("am_adam")
    with pytest.raises(V.VoiceAllowError):
        a.check_stratum("V-OTHER")
    assert a.check_chunk_mode("LOCKED-560-FLUSH") == "LOCKED-560-FLUSH"
    for bad in ("CHUNK-160", "CHUNK-1120"):
        with pytest.raises(V.VoiceAllowError):
            a.check_chunk_mode(bad, training=True)
        assert a.check_chunk_mode(bad, training=False) == bad
    assert set(a.job_names(["V-NL"])) == {"policy", "tool", "language", "runner", "carrier"}


def test_allow_list_sha_and_path_rules(tmp_path):
    m = tmp_path / "m.json"
    m.write_bytes(open(V.DEFAULT_MANIFEST, "rb").read())
    s = tmp_path / "m.sha256"
    s.write_text("1" * 64)
    with pytest.raises(V.VoiceAllowError):
        V.VoiceAllow(str(m), str(s))
    d = tmp_path / "x_ohs_y"
    d.mkdir()
    (d / "m.json").write_bytes(open(V.DEFAULT_MANIFEST, "rb").read())
    (d / "m.sha256").write_text(open(V.DEFAULT_MANIFEST_SHA).read())
    with pytest.raises(V.VoiceAllowError):
        V.VoiceAllow(str(d / "m.json"), str(d / "m.sha256"))


# ------------------------------------------------------------------ number words
@pytest.mark.parametrize("n", [0, 7, 13, 20, 21, 99, 100, 101, 110, 999, 1000, 1001, 12345, 100000, 1000000, 2500000])
def test_cardinal_and_ordinal_round_trip(n):
    assert NW._parse_cardinal(NW.cardinal(n)) == n
    if n:
        assert str(n) in NW.parse_number_tokens(NW.ordinal(n))


@pytest.mark.parametrize("y", [1100, 1900, 1905, 1999, 2000, 2005, 2026, 2099])
def test_years_round_trip(y):
    assert str(y) in NW.parse_number_tokens(NW.year_words(y))


def test_number_parser_rejects_invalid_grammar():
    for bad in ["four four three", "twenty twenty", "hundred", "one hundred hundred", "thirty twenty"]:
        c = NW.parse_number_tokens(bad.split())
        assert "11" not in c and "40" not in c and "46" not in c
    assert NW.parse_number_tokens("four four three".split()) == {"443"}
    assert NW.parse_number_tokens("three point eleven".split()) == {"3.11"}
    assert NW.parse_number_tokens("three point one one".split()) == {"3.11"}
    assert "2026" in NW.parse_number_tokens("twenty twenty six".split())


# ------------------------------------------------------------------ verbalizer
def test_symbol_table_covers_spec_symbols():
    for ch, word in {"/": "slash", ".": "dot", "-": "dash", "_": "underscore", "~": "tilde", "#": "hash", ":": "colon", "=": "equals", "*": "star"}.items():
        assert V.SYMBOL_WORDS[ch] == [word]
    d = VBZ.verbalize("rm -rf /tmp/build now please ok yes sure thanks", [], "V-DICT-LIT", rng(), check_length=False)
    assert d["tokens"][:6] == ["are", "em", "dash", "are", "eff", "slash"]
    d2 = VBZ.verbalize("a--b", [], "V-DICT-LIT", rng(), check_length=False)
    assert d2["tokens"] == ["ay", "dash", "dash", "bee"]


def test_every_spoken_token_is_known_zero_oov_leak():
    strings = PT.verbalizer_test_strings(1500, seed=1)
    n = 0
    for s in strings:
        try:
            d = VBZ.verbalize(s, [], "V-NL", rng(n), check_length=False)
        except V.Unspeakable:
            continue
        n += 1
        assert [t for t in d["tokens"] if not LEX.has(t)] == [], s
    assert n >= 1400


def test_unspeakable_symbols_are_refused_not_guessed():
    with pytest.raises(V.Unspeakable):
        VBZ.verbalize("café ☃ now and later today ok yes sure", [], "V-NL", rng(), check_length=False)


def test_oov_names_are_spelled_and_code_tokens_are_spelled():
    d = VBZ.verbalize("delete Kafetu and build_cache now please ok yes sure", [], "V-NL", rng(), check_length=False)
    assert "kafetu" not in d["tokens"] and d["tokens"][1:7] == ["kay", "ay", "eff", "ee", "tee", "you"]
    assert "underscore" in d["tokens"]


def test_uppercase_in_code_tokens_gets_capital_marker():
    d = VBZ.verbalize("run -R now and later today ok yes sure thanks", [], "V-DICT-LIT", rng(), check_length=False)
    i = d["tokens"].index("capital")
    assert d["tokens"][i + 1] == "are"


def test_length_gate_enforced():
    with pytest.raises(V.VoiceError):
        VBZ.verbalize("delete it", [], "V-NL", rng())
    long = " ".join(["delete"] * 420)
    with pytest.raises(V.VoiceError):
        VBZ.verbalize(long, [], "V-NL", rng())


def test_round_trip_with_test_oracle_on_5000_strings():
    strings = PT.verbalizer_test_strings(5200, seed=2)
    import vgates as G
    res = G.gate_c1_roundtrip(strings, VBZ, OD.denormalise)
    assert res["passed"], res["detail"]


def test_round_trip_harness_detects_a_broken_denormaliser():
    import vgates as G
    strings = PT.verbalizer_test_strings(300, seed=3)
    bad = lambda view: [t.upper() + "x" for t in OD.denormalise(view)]
    res = G.gate_c1_roundtrip(strings, VBZ, bad, min_strings=100)
    assert not res["passed"] and res["detail"]["bad_strings"] > 0


def test_public_view_hides_answers():
    d = VBZ.verbalize("push /tmp/x now and later today ok yes sure thanks", [], "V-DICT-LIT", rng(), check_length=False)
    v = VB.public_view(d)
    assert set(v) == {"tokens", "segments", "stratum"}
    assert all("char" not in s for s in v["segments"])
    assert any("char" in s for s in d["segments"])


def test_span_mapping_and_partial_flag():
    utt = "please do not delete /tmp/build with -rf now"
    i = utt.index("not")
    sp = [{"start": i, "end": i + 3, "text": "not", "role": "negation", "kind": "negation"},
          {"start": utt.index("/tmp") + 1, "end": utt.index("/tmp") + 4, "text": "tmp", "role": "entity", "kind": "path"}]
    d = VBZ.verbalize(utt, sp, "V-NL", rng(), check_length=False)
    assert d["tokens"][d["spans"][0]["tok"][0]:d["spans"][0]["tok"][1]] == ["not"]
    assert d["spans"][1]["partial"] and d["spans"][1]["canonical"] == "/tmp/build"


def test_span_that_covers_no_spoken_token_is_unspeakable():
    with pytest.raises(V.Unspeakable):
        VBZ.verbalize("a b c d e f g h i j k.", [{"start": 21, "end": 22, "text": ".", "role": "number", "kind": "number"}], "V-NL", rng(), check_length=False)


def test_fallback_spans_find_negations_numbers_paths():
    sp = VB.fallback_spans("please don't delete /var/log/app.log after 30 days with --force")
    kinds = {(s["role"], s["text"]) for s in sp}
    assert ("negation", "don't") in kinds and ("number", "30") in kinds and ("entity", "/var/log/app.log") in kinds and ("entity", "--force") in kinds


def test_natural_phrase_table_builds_spans_from_op_class_and_target():
    table = VB.NaturalPhraseTable({"ops": {"delete": ["remove the {target} {flags}", "get rid of the {target} {flags}"]}, "folder_words": ["folder"], "file_words": ["file"],
                                   "flag_phrases": {"-r": "recursively", "-f": "forcefully"}})
    text, spans = VB.natural_utterance("delete", "/tmp/buildCache", ["-r", "-f"], table, rng())
    assert "build cache folder in tmp" in text and "recursively" in text and "forcefully" in text
    assert {s["text"] for s in spans} >= {"build", "cache", "tmp", "recursively", "forcefully"}
    for s in spans:
        assert text[s["start"]:s["end"]] == s["text"] or s["kind"] == "rule"
    with pytest.raises(V.VoiceError):
        VB.natural_utterance("unknown_op", "/tmp/x", [], table, rng())


# ------------------------------------------------------------------ disfluency
def test_disfluency_keeps_spans_and_segments_consistent():
    utt = "please do not delete the cache on port 8080 and later today ok yes"
    sp = [{"start": utt.index("not"), "end": utt.index("not") + 3, "text": "not", "role": "negation", "kind": "negation"},
          {"start": utt.index("8080"), "end": utt.index("8080") + 4, "text": "8080", "role": "number", "kind": "number"}]
    base = VBZ.verbalize(utt, sp, "V-NL", rng(), check_length=False)
    n_ops = 0
    for k in range(200):
        d, ops = DF.apply_disfluency(base, DF.TEST_TABLE, rng(k), rate=1.0)
        n_ops += len(ops)
        for s in d["spans"]:
            assert d["tokens"][s["tok"][0]:s["tok"][1]] == base["tokens"][base["spans"][s["id"]]["tok"][0]:base["spans"][s["id"]]["tok"][1]]
        cover = sorted(t for seg in d["segments"] for t in range(seg["tok"][0], seg["tok"][1]))
        assert cover == list(range(len(d["tokens"])))
    assert n_ops > 100


def test_disfluency_rate_default_is_fifteen_percent():
    base = VBZ.verbalize("please do not delete the cache on port 8080 and later today ok yes", [], "V-NL", rng(), check_length=False)
    hit = sum(1 for k in range(2000) if DF.apply_disfluency(base, DF.TEST_TABLE, rng(k))[1])
    assert 0.10 < hit / 2000 < 0.20


# ------------------------------------------------------------------ WER and bands
def test_wer_basic_and_folds():
    assert W.wer("do not delete the cache", "do not delete the cache")[0] == 0
    assert abs(W.wer("do not delete the cache folder", "do not delete the cash folder")[0] - 1 / 6) < 1e-9
    assert W.wer("port eight zero eight zero", "port 8080.")[0] == 0
    assert W.wer("slash tmp slash build", "/tmp/build")[0] == 0
    assert W.wer("it costs twenty five dollars", "it costs 25 dollars")[0] == 0
    assert W.wer("before march fourteenth twenty twenty six", "before 2026-03-14")[0] == 0
    assert W.wer("hello", "")[0] == 1.0 and W.wer("", "")[0] == 0.0


def test_band_edges():
    assert [W.band_of(x) for x in (0.0, 0.029, 0.03, 0.079, 0.08, 0.149, 0.15, 0.249, 0.25, 0.9)] == [0, 0, 1, 1, 2, 2, 3, 3, None, None]


def test_dryrun_builds_twenty_in_memory_examples_and_writes_nothing(tmp_path, monkeypatch):
    import dryrun
    monkeypatch.chdir(tmp_path)
    ex = dryrun.build_examples()
    assert len(ex) == 20 and {e["generator"] for e in ex} == {"A", "B"}
    assert sum(1 for e in ex if e["kept"]) >= 12
    assert list(tmp_path.iterdir()) == []


def test_prepare_source_routes_strata_and_flags_fallback():
    table = VB.NaturalPhraseTable({"ops": {"delete": ["please remove the {target} {flags}"]}, "folder_words": ["folder"], "file_words": ["file"], "flag_phrases": {"-r": "recursively"}})
    u = "please do not delete the cache folder now and later today"
    assert VB.prepare_source(u, [{"start": 10, "end": 13, "text": "not", "role": "negation", "kind": "negation"}], None, "V-NL", rng(), None)[2] is False
    t, sp, fb = VB.prepare_source(u, None, None, "V-NL", rng(), None)
    assert fb is True and any(s["text"] == "not" for s in sp)
    assert VB.prepare_source(u, None, None, "V-DICT-NAT", rng(), table) is None
    t, sp, fb = VB.prepare_source(u, None, {"op_class": "delete", "target": "/tmp/buildCache", "flags": ["-r"]}, "V-DICT-NAT", rng(), table)
    assert "build cache folder in tmp" in t and fb is False and sp
    d = VBZ.verbalize(t, sp, "V-DICT-NAT", rng(), check_length=False)
    assert SC.check_doc(d, t)["kept"]


def test_unsupported_span_kinds_are_refused():
    with pytest.raises(V.Unspeakable):
        VBZ.verbalize("starts at 2026-03-01 08:30 UTC+02:00 now and later today ok", [{"start": 10, "end": 38, "text": "2026-03-01 08:30 UTC+02:00", "role": "number", "kind": "datetime"}], "V-NL", rng(), check_length=False)
