"""CHECK EACH VOICE VARIANT AT THE MOMENT IT IS MADE (OWNER RULE, 18 Oct 2026; plan 16.1 steps 0, 2, 3, 6, 7; VOICE addendum v3.2 section 3).

    "If you're building one row, check that row at that same point and that's it ... then train."

CODE ONLY. No audio, no TTS, no ASR run here: the GPU steps (Kokoro, the pinned Nemotron) happen on od-l4b and hand their TRANSCRIPT in as `hyp`
(generator A) or the noiser / phoneme-swap code makes it on the CPU (B, C). This module decides whether a made variant may enter the pool. It writes
nothing, prints no text, calls no model, spawns no process, executes no generated code.

Per variant (all must pass; a failure DROPS the variant, never edits it; gold is inherited and never relabelled):
  (a0) source       the SOURCE row carries a CURRENT clean stamp (registry sha equal to the pinned one), has program or execution gold (not a human-label
                    row, A46), its family is not rolled, it is not an L-R row, a C2 replay source only after the replay clean-up, and the verbalized
                    utterance has 10-400 tokens
  (a1) verbalizer   solver B's DENORMALISER recovers the written tokens of THIS utterance from the spoken form, token for token
  (a2) spans        BOTH span-survival checkers (A: word alignment, B: character / key matching) say every decision-bearing span survived and that no
                    negation or polarity word appeared or vanished; any disagreement drops the variant (logged by role)
  (a3) ctx exception OFF: a deleted or garbled span ALWAYS drops the variant (flag `ctx_recoverable_enabled` must be False in C2.1); rows on the
                    fallback regex never use it
  (a4) generator    A: the raw ASR text is recorded as emitted, a chunk mode of LOCKED-560-FLUSH only, a voice on the grade-C allow-list;
                    B: the substitution list is recorded; C: refused unless the dictionary licence record passes V-C11 and every swap is within one phoneme
  (a5) WER + tokens measured WER by B's OWN edit distance is in a kept band (< 25 percent); transcript <= 1,536 tokens
  (a6) guards       PII scrub and the C_DATA_SPEC literals on the transcript AND the whole row text
  (b)  G13 stamp    the transcript field AND the whole row go to the stamp service (two items per variant, batches of <= 500); a hit drops the variant
  (c)  stamp record {variant_id, source_row_id, source stamp ref, generator, registry_sha, method_set_version, code sha, table hashes, verdict}
  (m)  at the mix   `mix_guard`: a voice row whose clean twin is not in the mix, or whose stamp (or its twin's) is stale, is refused

Drop logs hold ids, reason codes, roles and G13 target NAMES and METHODS only, never row text or matched text.
"""
import collections
import hashlib
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(os.path.dirname(HERE), "GEN")
SOLVER_B = os.path.join(HERE, "solver_b")
for _p in (HERE, GEN):
    if _p not in sys.path:
        sys.path.insert(0, _p)
if SOLVER_B not in sys.path:
    sys.path.append(SOLVER_B)

import span_check as SC                                                                          # noqa: E402
import verbalizer as V                                                                            # noqa: E402
import vcommon as C                                                                               # noqa: E402
import wer as W                                                                                   # noqa: E402
from stamp_hook import (ConformanceRecordRequired, RefusingHook, RowGuardRequired, StampServiceRequired, guard_facts)   # noqa: E402,F401

import vb_check as BC                                                                             # noqa: E402  (solver B)
import vb_wer as BW                                                                               # noqa: E402
from vb_denorm import DenormError, denormalise                                                    # noqa: E402

BATCH = 500
MAX_TOKENS = 1536
FIX_TRIGGER_RATE = 0.01
CTX_RECOVERABLE_ENABLED = False                    # Opus VOICE-B1: OFF in C2.1; flipping it needs a ruling and the gold re-run callback below

REASONS = ("source_stamp", "source_human_label", "source_rolled", "source_lr", "source_replay_uncleaned", "length", "denorm", "denorm_error",
           "spans_A", "spans_B", "A_B_disagree", "ctx_exception_on", "generator", "chunk_mode", "voice", "licence", "band", "tokens", "pii",
           "guard_literal", "twin")

_PII = [re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"), re.compile(r"https?://", re.I), re.compile(r"\b\d{3}[- ]\d{2}[- ]\d{4}\b"), re.compile(r"\+\d{1,3}[ -]?\d{6,}")]
_LITERALS = [re.compile(p, re.I) for p in (
    r"\bCVE-\d{4}-\d{3,}", r"\bGHSA-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}", r"rosetta", r"stackoverflow", r"stackexchange", r"BENCHMARK DATA", r"canary GUID",
    r"lm-eval", r"lm_eval", r"opencompass", r"big-?bench", r"leetcode", r"\bgsm-?8k\b", r"\bmmlu\b", r"\bhumaneval\b", r"\bjevbench\b")]


class VariantChecker(object):
    """check_variant(source, variant) -> (reasons, notes).

    source   {"row_id", "family", "label", "stamp": {"registry_sha", "verdict"}, "human_label": bool, "rolled": bool, "lr": bool,
              "replay": bool, "replay_cleaned": bool, "text": whole-row text (for the guards), "utterance_spans_exported": bool}
    variant  {"variant_id", "source_row_id", "generator": "A"|"B"|"C", "doc": SpokenDoc (verbalizer output), "hyp": transcript text,
              "stratum", "voice", "chunk_mode", "raw_asr": str (A), "ops": list (B), "swaps": list of (word, word, phoneme distance) (C)}"""

    def __init__(self, registry_sha, allow=None, c_licence_record=None, ctx_recoverable_enabled=CTX_RECOVERABLE_ENABLED):
        self.registry_sha = registry_sha
        self.allow = allow or C.VoiceAllow()
        self.c_ok = C.dictionary_licence_ok(c_licence_record)
        self.ctx_enabled = bool(ctx_recoverable_enabled)

    def check_variant(self, source, variant):
        reasons, notes = [], []
        # (a0)
        st = source.get("stamp") or {}
        if st.get("verdict") != "clean" or st.get("registry_sha") != self.registry_sha:
            reasons.append("source_stamp")
        if source.get("human_label"):
            reasons.append("source_human_label")
        if source.get("rolled"):
            reasons.append("source_rolled")
        if source.get("lr"):
            reasons.append("source_lr")
        if source.get("replay") and not source.get("replay_cleaned"):
            reasons.append("source_replay_uncleaned")
        doc = variant["doc"]
        n_tok = len(doc["tokens"])
        if not (C.MIN_VERB_TOKENS <= n_tok <= C.MAX_VERB_TOKENS):
            reasons.append("length")
        # (a1) the independent denormaliser on THIS utterance
        try:
            got = [t.lower() for t in denormalise(V.public_view(doc))]
            if got != [t.lower() for t in doc["source_tokens"]]:
                reasons.append("denorm")
        except DenormError:
            reasons.append("denorm_error")
        except Exception:      # noqa: BLE001
            reasons.append("denorm_error")
        # (a2)/(a3) both span checkers, flag OFF
        if self.ctx_enabled:
            reasons.append("ctx_exception_on")                 # needs the gold re-run callback, which C2.1 does not wire
        hyp = variant["hyp"]
        ra = SC.check_doc(doc, hyp)
        try:
            rb = BC.check_detail(doc, hyp)
        except Exception:      # noqa: BLE001
            rb = {"kept": False, "reasons": ["b_error"]}
        if not ra["kept"]:
            reasons.append("spans_A")
        if not rb["kept"]:
            reasons.append("spans_B")
        if ra["kept"] != rb["kept"]:
            reasons.append("A_B_disagree")
        if any(sp.get("fallback") for sp in doc["spans"]):
            notes.append("fallback_spans")
        # (a4) generator-specific
        g = variant["generator"]
        if g == "A":
            if variant.get("chunk_mode") != C.CHUNK_MODE_TRAINING:
                reasons.append("chunk_mode")
            try:
                self.allow.check_voice(variant.get("voice"))
            except Exception:      # noqa: BLE001
                reasons.append("voice")
            if not isinstance(variant.get("raw_asr"), str) or variant["raw_asr"] != hyp:
                reasons.append("generator")                       # the transcript must be the raw ASR text exactly as emitted
        elif g == "B":
            if "ops" not in variant:
                reasons.append("generator")
        elif g == "C":
            if not self.c_ok:
                reasons.append("licence")
            elif any(d > 1 for _w, _v, d in variant.get("swaps", [])) or not variant.get("swaps_checked_by_B"):
                reasons.append("generator")
        else:
            reasons.append("generator")
        try:
            self.allow.check_stratum(variant["stratum"])
        except Exception:      # noqa: BLE001
            reasons.append("generator")
        # (a5) WER band by B's own edit distance; transcript length
        w = BW.wer(doc, hyp, fine=False)
        variant["wer_B"], variant["band"] = w, BW.band_of(w)
        if BW.band_of(w) is None:
            reasons.append("band")
        if len(hyp.split()) > MAX_TOKENS:
            reasons.append("tokens")
        # (a6) guards on the transcript and the whole row
        text = hyp + "\n" + (source.get("text") or "")
        if any(p.search(text) for p in _PII):
            reasons.append("pii")
        if any(p.search(text) for p in _LITERALS):
            reasons.append("guard_literal")
        return list(dict.fromkeys(reasons)), notes


def code_sha(extra_files=()):
    h = hashlib.sha256()
    files = [os.path.join(HERE, f) for f in sorted(os.listdir(HERE)) if f.endswith(".py")]
    files += [os.path.join(SOLVER_B, f) for f in sorted(os.listdir(SOLVER_B)) if f.endswith(".py")] + list(extra_files)
    for p in files:
        with open(p, "rb") as f:
            h.update(hashlib.sha256(f.read()).hexdigest().encode("ascii"))
    return h.hexdigest()


def _items(variants, sources, sha):
    out = []
    for v in variants:
        out.append(dict(row_id=v["variant_id"] + ":transcript", family="VOICE", text=v["hyp"], generator_sha=sha))
        out.append(dict(row_id=v["variant_id"] + ":row", family="VOICE", text=v["hyp"] + "\n" + (sources[v["source_row_id"]].get("text") or ""), generator_sha=sha))
    return out


def check_and_stamp(variants, sources, checker, stamper, standin=True, environ=None, conformance_ok=None, table_hashes=None, batch=BATCH):
    """Run the per-variant checks, then the G13 stamp in batches of <= 500 variants. Returns (kept, summary, log).
    A variant needs its source (by id) in `sources`. A source that fails a stamp or an answer check never produces a variant."""
    if stamper is None or isinstance(stamper, RefusingHook):
        raise StampServiceRequired("no G13 stamp service wired: no voice variant may enter the pool unstamped")
    guard = None
    if not standin:
        if getattr(stamper, "is_test_double", False):
            raise StampServiceRequired("a test double cannot stamp a production run")
        guard = guard_facts(getattr(checker.allow, "sha", None), environ)
        if conformance_ok is None or not conformance_ok(code_sha()):
            raise ConformanceRecordRequired("no signed conformance record for the current code sha")
    sha = code_sha()
    S = collections.Counter()
    drops = collections.Counter()
    log = []
    passed = []
    for v in variants:
        S["made"] += 1
        src = sources.get(v["source_row_id"])
        if src is None:
            drops[("answer", "source_stamp")] += 1
            log.append(dict(variant_id=v["variant_id"], stage="answer", reasons=["source_stamp"]))
            continue
        why, notes = checker.check_variant(src, v)
        for n in notes:
            S["note:" + n] += 1
        if why:
            for w in why:
                drops[("answer", w)] += 1
            log.append(dict(variant_id=v["variant_id"], source_row_id=v["source_row_id"], generator=v["generator"], stage="answer", reasons=why,
                            roles=sorted({r.split(":")[0] for r in (SC.check_doc(v["doc"], v["hyp"])["reasons"])})))
            continue
        passed.append(v)
    kept = []
    for i in range(0, len(passed), batch):
        chunk = passed[i:i + batch]
        S["stamp_calls"] += 1
        verdicts = stamper.stamp(_items(chunk, sources, sha))
        for v in chunk:
            bad = None
            for suffix in (":transcript", ":row"):
                vd = verdicts.get(v["variant_id"] + suffix)
                if vd is None or vd.get("verdict") == "error" or (guard and vd.get("registry_sha") != guard["registry_sha"]):
                    bad = ("stamp_error", vd or {})
                    break
                if vd.get("verdict") == "hit" and any(not h.get("exempt") for h in vd.get("hits", [])):
                    bad = ("g13_hit", vd)
                    break
            if bad:
                drops[("g13", bad[0])] += 1
                log.append(dict(variant_id=v["variant_id"], source_row_id=v["source_row_id"], stage="g13", reasons=[bad[0]],
                                hits=[dict(target=h.get("target"), method=h.get("method"), exempt=h.get("exempt")) for h in bad[1].get("hits", [])]))
                continue
            vd = verdicts[v["variant_id"] + ":row"]
            v["stamp"] = dict(variant_id=v["variant_id"], source_row_id=v["source_row_id"], source_stamp_ref=(sources[v["source_row_id"]].get("stamp") or {}).get("registry_sha"),
                              generator=v["generator"], registry_sha=vd.get("registry_sha"), method_set_version=vd.get("method_set_version"), code_sha=sha,
                              table_hashes=table_hashes, verdict="clean")
            kept.append(v)
    g13 = sum(n for (s, _r), n in drops.items() if s == "g13")
    summary = dict(made=S["made"], kept=len(kept), dropped={"%s:%s" % k: n for k, n in sorted(drops.items())}, stamp_calls=S["stamp_calls"],
                   notes={k: n for k, n in S.items() if k.startswith("note:")}, g13_drop_rate=round(g13 / S["made"], 5) if S["made"] else 0.0,
                   fix_trigger_g13=(g13 / S["made"] > FIX_TRIGGER_RATE) if S["made"] else False)
    return kept, summary, log


def mix_guard(variants, mix_row_ids, current_registry_sha):
    """Step 7 for voice rows: a variant enters the mix only with its clean text twin (the SOURCE row) in the mix and a current stamp on both.
    Returns (accepted, refused[(variant_id, reason)])."""
    ok, bad = [], []
    for v in variants:
        st = v.get("stamp") or {}
        if v["source_row_id"] not in mix_row_ids:
            bad.append((v["variant_id"], "twin"))
        elif st.get("verdict") != "clean" or st.get("registry_sha") != current_registry_sha or st.get("source_stamp_ref") != current_registry_sha:
            bad.append((v["variant_id"], "source_stamp"))
        else:
            ok.append(v)
    return ok, bad
