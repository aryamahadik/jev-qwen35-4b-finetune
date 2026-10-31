"""CHECK-AT-CREATION tests for VOICE (owner rule 18 Oct 2026). Synthetic sources only (planted.py); no audio, no TTS, no ASR, no model."""
import os
import random

import pytest

import noiser as NS
import planted as PT
import voice_check as VC
import vcommon as C
from gen_common import RowNamer
from stamp_hook import StampHook, TestDoubleHook

REG = "r" * 64
VOICE_OK = "af_heart"


def _make(k, gen="A", stratum="V-NL", alter=None, seed="vrc"):
    rng = random.Random("%s-%d" % (seed, k))
    namer = RowNamer("%s-%d" % (seed, k))
    doc = PT.make_doc(rng, namer, k, stratum)
    chunks = PT.render_chunks(doc, rng)
    if alter:
        assert alter(doc, chunks, rng)
    hyp = PT.join_chunks(chunks, rng)
    src = {"row_id": "S%d" % k, "family": "T50", "label": "A", "stamp": {"registry_sha": REG, "verdict": "clean"}, "human_label": False, "rolled": False,
           "lr": False, "replay": False, "replay_cleaned": False, "text": "options A B C; card text"}
    var = {"variant_id": "V%d" % k, "source_row_id": src["row_id"], "generator": gen, "doc": doc, "hyp": hyp, "stratum": stratum, "voice": VOICE_OK,
           "chunk_mode": C.CHUNK_MODE_TRAINING, "raw_asr": hyp, "ops": []}
    if gen == "B":
        var.pop("raw_asr"), var.pop("voice")
    return src, var


@pytest.fixture(scope="module")
def checker():
    return VC.VariantChecker(REG)


def test_clean_variants_pass_and_get_a_stamp_record(checker):
    pairs = [_make(k, "A" if k % 2 == 0 else "B", ["V-NL", "V-DICT-LIT", "V-NUM"][k % 3]) for k in range(30)]
    sources = {s["row_id"]: s for s, _ in pairs}
    kept, summ, log = VC.check_and_stamp([v for _, v in pairs], sources, checker, TestDoubleHook(registry_sha=REG), standin=True)
    assert summ["kept"] == len(kept) and summ["kept"] >= 25, summ
    for v in kept:
        assert v["stamp"]["verdict"] == "clean" and v["stamp"]["source_stamp_ref"] == REG and v["stamp"]["generator"] == v["generator"]
        assert v["band"] is not None
    assert all(l["stage"] == "answer" for l in log)


@pytest.mark.parametrize("name,mut,reason", [
    ("stale_source_stamp", lambda s, v: s["stamp"].__setitem__("registry_sha", "x" * 64), "source_stamp"),
    ("human_label_source", lambda s, v: s.__setitem__("human_label", True), "source_human_label"),
    ("rolled_family", lambda s, v: s.__setitem__("rolled", True), "source_rolled"),
    ("l_r_source", lambda s, v: s.__setitem__("lr", True), "source_lr"),
    ("replay_not_cleaned", lambda s, v: s.update(replay=True, replay_cleaned=False), "source_replay_uncleaned"),
    ("wrong_chunk_mode", lambda s, v: v.__setitem__("chunk_mode", "CHUNK-160"), "chunk_mode"),
    ("voice_off_list", lambda s, v: v.__setitem__("voice", "am_adam"), "voice"),
    ("asr_text_edited", lambda s, v: v.__setitem__("raw_asr", v["hyp"] + " extra"), "generator"),
    ("pii_in_row", lambda s, v: s.__setitem__("text", "mail a@b.example"), "pii"),
    ("literal_in_transcript", lambda s, v: v.__setitem__("hyp", v["hyp"] + " CVE-2024-12345"), "guard_literal"),
])
def test_planted_defect_drops_the_variant(checker, name, mut, reason):
    src, var = _make(3, "A")
    mut(src, var)
    if name == "literal_in_transcript":
        var["raw_asr"] = var["hyp"]
    why, _ = checker.check_variant(src, var)
    assert reason in why, (name, why)


def test_altered_span_is_dropped_by_both_checkers(checker):
    hits = 0
    for k in range(40):
        src, var = _make(k, "A", alter=lambda d, c, r: PT.alter(d, c, r))
        why, _ = checker.check_variant(src, var)
        if why:
            assert "spans_A" in why and "spans_B" in why or "A_B_disagree" in why, why
            hits += 1
    assert hits >= 30


def test_polarity_word_inserted_anywhere_is_dropped(checker):
    src, var = _make(5, "B")
    toks = var["hyp"].split()
    var["hyp"] = " ".join(toks[:1] + ["except"] + toks[1:])
    why, _ = checker.check_variant(src, var)
    assert "spans_A" in why


def test_context_recoverable_exception_is_off_and_cannot_be_switched_on_silently():
    assert VC.CTX_RECOVERABLE_ENABLED is False
    ck = VC.VariantChecker(REG, ctx_recoverable_enabled=True)
    src, var = _make(2, "A")
    why, _ = ck.check_variant(src, var)
    assert "ctx_exception_on" in why


def test_generator_c_is_refused_without_a_dictionary_licence_record(checker):
    src, var = _make(4, "B")
    var["generator"] = "C"
    var["swaps"] = [("a", "b", 1)]
    var["swaps_checked_by_B"] = True
    why, _ = checker.check_variant(src, var)
    assert "licence" in why
    ok = VC.VariantChecker(REG, c_licence_record={"spdx": "MIT", "quote": "q", "url": "u", "fetched": "2026-10-18"})
    why, _ = ok.check_variant(src, var)
    assert "licence" not in why
    nc = VC.VariantChecker(REG, c_licence_record={"spdx": "CC-BY-NC-4.0", "quote": "q", "url": "u", "fetched": "d"})
    assert "licence" in nc.check_variant(src, var)[0]


def test_generator_shares_follow_the_licence_record():
    assert C.generator_shares(None) == {"A": 0.55, "B": 0.45}
    assert C.generator_shares({"spdx": "GPL-3.0", "quote": "q", "url": "u", "fetched": "d"}) == {"A": 0.55, "B": 0.45}
    assert C.generator_shares({"spdx": "Apache-2.0", "quote": "q", "url": "u", "fetched": "d"}) == {"A": 0.50, "B": 0.30, "C": 0.20}


def test_g13_hit_drops_the_variant_and_logs_names_only(checker):
    pairs = [_make(k, "B") for k in range(8)]
    sources = {s["row_id"]: s for s, _ in pairs}
    variants = [v for _, v in pairs]
    first = [v for v in variants if not checker.check_variant(sources[v["source_row_id"]], v)[0]][0]
    stamper = TestDoubleHook(hit_ids=[first["variant_id"] + ":transcript"], registry_sha=REG)
    kept, summ, log = VC.check_and_stamp(variants, sources, checker, stamper, standin=True)
    g = [l for l in log if l["stage"] == "g13"]
    assert len(g) == 1 and g[0]["variant_id"] == first["variant_id"] and g[0]["hits"][0]["target"] == "target.test"
    assert first["variant_id"] not in {v["variant_id"] for v in kept}
    dumped = str(log)
    assert "hyp" not in dumped and "tokens" not in dumped


def test_both_fields_are_stamped_and_a_hit_on_the_whole_row_also_drops(checker):
    src, var = _make(1, "B")
    stamper = TestDoubleHook(hit_ids=[var["variant_id"] + ":row"], registry_sha=REG)
    kept, summ, log = VC.check_and_stamp([var], {src["row_id"]: src}, checker, stamper, standin=True)
    assert not kept and summ["dropped"].get("g13:g13_hit") == 1


def test_no_hook_no_variants_and_production_guards(checker):
    src, var = _make(0, "B")
    with pytest.raises(VC.StampServiceRequired):
        VC.check_and_stamp([var], {src["row_id"]: src}, checker, None)
    with pytest.raises(VC.StampServiceRequired):
        VC.check_and_stamp([var], {src["row_id"]: src}, checker, VC.RefusingHook())
    with pytest.raises(VC.StampServiceRequired):
        VC.check_and_stamp([var], {src["row_id"]: src}, checker, TestDoubleHook(), standin=False)

    class Real(StampHook):
        def stamp(self, items):
            return {}
    with pytest.raises(VC.RowGuardRequired):
        VC.check_and_stamp([var], {src["row_id"]: src}, checker, Real(), standin=False, environ={})
    env = {"OD_ROWGUARD_FREEZE_SHA": "f" * 64, "OD_ROWGUARD_REGISTRY_SHA": REG, "OD_ROWGUARD_ALLOWLIST_SHA": checker.allow.sha}
    with pytest.raises(VC.ConformanceRecordRequired):
        VC.check_and_stamp([var], {src["row_id"]: src}, checker, Real(), standin=False, environ=env)


def test_batches_of_at_most_500_variants(checker):
    pairs = [_make(k, "B") for k in range(60)]
    sources = {s["row_id"]: s for s, _ in pairs}
    sizes = []

    class Count(TestDoubleHook):
        def stamp(self, items):
            sizes.append(len(items))
            return super().stamp(items)
    VC.check_and_stamp([v for _, v in pairs], sources, checker, Count(registry_sha=REG), standin=True, batch=20)
    assert sizes and max(sizes) <= 40            # two items per variant, 20 variants per batch


def test_mix_guard_needs_the_clean_twin_and_a_current_stamp(checker):
    src, var = _make(6, "B")
    kept, _s, _l = VC.check_and_stamp([var], {src["row_id"]: src}, checker, TestDoubleHook(registry_sha=REG), standin=True)
    assert kept
    ok, bad = VC.mix_guard(kept, {src["row_id"]}, REG)
    assert ok and not bad
    ok, bad = VC.mix_guard(kept, set(), REG)
    assert not ok and bad[0][1] == "twin"
    ok, bad = VC.mix_guard(kept, {src["row_id"]}, "z" * 64)
    assert not ok and bad[0][1] == "source_stamp"


def test_confusion_table_harvest_refuses_dev_and_test_audio():
    pairs = [(["a", "delete", "b"], ["a", "deleted", "b"])]
    t = NS.harvest_table(pairs, source="LibriSpeech Nemotron", splits=["train-clean-100", "train-other-500"])
    assert NS.ConfusionTable(t).is_production() and t["splits"] == ["train-clean-100", "train-other-500"]
    for bad in (["test-clean"], ["dev-other"], ["train-clean-100", "test-other"], []):
        with pytest.raises(C.VoiceError):
            NS.harvest_table(pairs, source="LibriSpeech Nemotron", splits=bad)
    with pytest.raises(C.VoiceError):
        NS.harvest_table(pairs, source="LibriSpeech Nemotron")        # a real source must name its splits
    assert not NS.ConfusionTable(NS.harvest_table(pairs)).is_production()


def test_dictated_natural_refuses_a_non_path_operation_and_an_unknown_flag():
    import json
    import os
    import verbalizer as V
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pools", "natural_phrase_table.json")) as f:
        table = V.NaturalPhraseTable(json.load(f))
    rng = random.Random(1)
    text, spans = V.natural_utterance("delete", "/tmp/build", ["-r"], table, rng)
    assert "recursively" in text and spans
    with pytest.raises(C.VoiceError):
        V.natural_utterance("restart", "nginx", [], table, rng)          # a service, not a path
    with pytest.raises(C.VoiceError):
        V.natural_utterance("delete", "/tmp/build", ["-n"], table, rng)  # no phrase: the paraphrase would silently drop the flag


def test_possessive_of_a_known_word_is_not_unspeakable():
    import verbalizer as V
    lex = C.test_lexicon()
    assert lex.has("number's") and not lex.has("zzyzx's") and not lex.has("'s")
    doc = V.Verbalizer(lex).verbalize("Delete the number's cache and the file today please", [], "V-NL", random.Random(1), check_length=False)
    assert "number's" in doc["tokens"]


def test_gen_rows_feed_the_voice_lane_through_the_decision_span_contract():
    """G10: the spans a GEN row exports are consumable by the verbalizer and the checker (a perfect transcript keeps every span)."""
    import sys
    gen = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "GEN")
    sys.path.insert(0, gen)
    import builder as BU
    import gen_common as g
    import span_check as SC
    import verbalizer as V
    pool = g.make_testonly_pool()
    b = BU.Builder("vint", pool, provisional=True, mode="dry")
    lex = C.test_lexicon()
    n = kept = 0
    for form in ("AR-F1", "AR-F2", "TM-T1"):
        for i in range(120):
            for r in b.unit(form, "train", i, pair_prob=0.0):
                if not r["voice_eligible"]:
                    continue
                try:
                    doc = V.Verbalizer(lex).verbalize(r["stem"], r["decision_spans"], "V-NL", random.Random(i))
                except C.VoiceError:
                    continue
                n += 1
                kept += SC.check_doc(doc, doc["tts_text"])["kept"]
    assert n >= 5 and kept == n
