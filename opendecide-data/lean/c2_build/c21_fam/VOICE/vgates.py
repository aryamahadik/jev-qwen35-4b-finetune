"""VOICE PRE-FREEZE CPU gates (G0-lite VOICE section 5, Opus rulings). Data and code only: no audio, no TTS run, no ASR run.

Here: V-C1 verbalizer round trip (harness for solver B's denormaliser), V-C2 zero OOV leakage and no espeak-ng / no subprocess,
V-C3 misaki front end with the espeak-ng fallback off (runs only when misaki is installed; reports NOT_RUN otherwise),
V-C4 span checker on planted edits (harness for solver A and solver B), V-C5 metadata coverage, V-C6 label drift,
V-C7 surface probes, V-C8 size and share rules, V-C9 noiser calibration (with a caller-supplied independent WER), V-C10 length.
The data-production gates V-D1..V-D7 are the pure decision functions in pool.py (they consume measurements from the L4 jobs).
Each gate returns {"gate", "class", "passed", "detail"}.
"""
import collections
import os
import random

import numpy as np

import pool as PL
import span_check as SC
import wer as W
from vcommon import (BAND_SHARE, BAND_TOL, FALLBACK_SPAN_CAP, MAX_VARIANTS_PER_SOURCE, MAX_VERB_TOKENS, MIN_VERB_TOKENS, STRATA, Lexicon,
                     VoiceAllow, table_hashes)

import planted as PT  # noqa: E402


def _res(gate, passed, detail, cls="PK"):
    return {"gate": gate, "class": cls, "passed": bool(passed), "detail": detail}


# ------------------------------------------------------------------------------------------------
# V-C1 verbalizer round trip
# ------------------------------------------------------------------------------------------------
def gate_c1_roundtrip(strings, verbalizer, denormalise, seed=0, min_strings=5000):
    """denormalise(view) -> list of written tokens, from view['tokens'] and view['segments'] only (solver B's code; see verbalizer.public_view).
    Must equal doc['source_tokens'] lower-cased, token for token, on 100 percent of tokens. Unspeakable strings are counted and skipped."""
    rng = random.Random("c1-%s" % seed)
    ok_tok = tot_tok = bad = skipped = 0
    bad_ids = []
    for i, s in enumerate(strings):
        try:
            doc = verbalizer.verbalize(s, [], rng.choice(STRATA[:2] + STRATA[3:]), rng, check_length=False)
        except Exception:
            skipped += 1
            continue
        from verbalizer import public_view
        got = [t.lower() for t in denormalise(public_view(doc))]
        exp = [t.lower() for t in doc["source_tokens"]]
        tot_tok += len(exp)
        ok_tok += sum(1 for a, b in zip(got, exp) if a == b) if len(got) == len(exp) else 0
        if got != exp:
            bad += 1
            bad_ids.append(i)
    n = len(strings) - skipped
    return _res("V-C1", tot_tok > 0 and ok_tok == tot_tok and n >= min_strings,
                {"strings": len(strings), "tested": n, "skipped_unspeakable": skipped, "token_accuracy": ok_tok / max(1, tot_tok), "bad_strings": bad, "bad_ids": bad_ids[:10],
                 "min_strings": min_strings})


# ------------------------------------------------------------------------------------------------
# V-C2 no OOV leakage, espeak-ng absent, no subprocess
# ------------------------------------------------------------------------------------------------
def espeak_on_path():
    found = []
    for d in os.environ.get("PATH", "").split(os.pathsep):
        for name in ("espeak-ng", "espeak"):
            p = os.path.join(d, name)
            if d and os.path.isfile(p):
                found.append(p)
    return found


class NoSpawn:
    """While active, subprocess.Popen, os.system and os.popen raise: proves the verbalizer / checker spawn nothing."""

    def __enter__(self):
        import subprocess
        self._sp, self._sys, self._popen = subprocess.Popen, os.system, os.popen

        def boom(*a, **k):
            raise RuntimeError("process spawn attempted")
        subprocess.Popen = boom
        os.system = boom
        os.popen = boom
        return self

    def __exit__(self, *exc):
        import subprocess
        subprocess.Popen, os.system, os.popen = self._sp, self._sys, self._popen
        return False


def unknown_tokens(doc, lexicon):
    return [t for t in doc["tokens"] if not lexicon.has(t)]


def gate_c2_oov(strings, verbalizer, lexicon, seed=0, min_strings=5000):
    rng = random.Random("c2-%s" % seed)
    leaked = collections.Counter()
    tested = skipped = 0
    with NoSpawn():
        for s in strings:
            try:
                doc = verbalizer.verbalize(s, [], rng.choice(STRATA[:2] + STRATA[3:]), rng, check_length=False)
            except Exception:
                skipped += 1
                continue
            tested += 1
            for t in unknown_tokens(doc, lexicon):
                leaked[t] += 1
    esp = espeak_on_path()
    return _res("V-C2", not leaked and not esp and tested >= min_strings,
                {"tested": tested, "skipped_unspeakable": skipped, "leaked_tokens": dict(list(leaked.items())[:10]), "n_leaked": sum(leaked.values()),
                 "espeak_on_path": esp, "min_strings": min_strings})


# ------------------------------------------------------------------------------------------------
# V-C3 misaki front end with the fallback off (never downloads anything; the synthesis half runs on od-l4b)
# ------------------------------------------------------------------------------------------------
def gate_c3_misaki(strings):
    try:
        from misaki import en  # noqa: F401
    except Exception as e:                                           # not installed on this Mac
        return _res("V-C3", False, {"status": "NOT_RUN", "reason": "misaki is not installed (%s)" % type(e).__name__,
                                    "next": "install on od-l4b, run this function with 500 test strings; then the Kokoro synthesis half"})
    bad = []
    with NoSpawn():
        g2p = en.G2P(trf=False, british=False, fallback=None)
        for s in strings:
            try:
                ph, _ = g2p(s)
            except Exception as e:
                bad.append((s, type(e).__name__))
                continue
            if not ph or "❓" in ph:                              # empty output or the unknown-word marker
                bad.append((s, "empty_or_unknown_marker"))
    return _res("V-C3", not bad and len(strings) >= 500, {"tested": len(strings), "bad": bad[:10], "status": "RAN", "synthesis_half": "not run here (needs Kokoro weights)"})


# ------------------------------------------------------------------------------------------------
# V-C4 span checker on planted edits (solver A and solver B each; agreement)
# ------------------------------------------------------------------------------------------------
def planted_metrics(cases, check):
    """check(doc, hyp_text) -> bool kept. Returns recall on alterations, false-alarm rate on benign equivalents, per-edit misses."""
    n_alt = n_alt_caught = n_ben = n_ben_dropped = 0
    miss, fa = collections.Counter(), collections.Counter()
    verdicts = []
    for c in cases:
        kept = bool(check(c["doc"], c["hyp"]))
        verdicts.append(kept)
        if c["expect_kept"]:
            n_ben += 1
            if not kept:
                n_ben_dropped += 1
                fa[c["edit"]] += 1
        else:
            n_alt += 1
            if kept:
                miss[c["edit"]] += 1
            else:
                n_alt_caught += 1
    return {"n_alter": n_alt, "recall": n_alt_caught / max(1, n_alt), "recall_wilson_lb": PL.wilson_lower(n_alt_caught, n_alt), "n_benign": n_ben,
            "false_alarm": n_ben_dropped / max(1, n_ben), "misses": dict(miss), "false_alarms": dict(fa), "verdicts": verdicts}


def gate_c4_planted(check_a=None, check_b=None, n_alter=2000, n_benign=1200, seed=0, cases=None):
    cases = cases or PT.planted_suite(n_alter, n_benign, seed)
    check_a = check_a or (lambda doc, hyp: SC.check_doc(doc, hyp)["kept"])
    ma = planted_metrics(cases, check_a)
    det = {"A": {k: v for k, v in ma.items() if k != "verdicts"}}
    ok = ma["n_alter"] >= 2000 and ma["recall"] >= 0.99 and ma["recall_wilson_lb"] >= 0.97 and ma["false_alarm"] <= 0.01
    if check_b is not None:
        mb = planted_metrics(cases, check_b)
        det["B"] = {k: v for k, v in mb.items() if k != "verdicts"}
        agree = sum(1 for a, b in zip(ma["verdicts"], mb["verdicts"]) if a == b) / len(cases)
        det["agreement"] = agree
        ok = ok and mb["recall"] >= 0.99 and mb["recall_wilson_lb"] >= 0.97 and mb["false_alarm"] <= 0.01 and agree >= 0.995
    else:
        det["B"] = "not supplied: solver B runs the same cases in its own session"
        ok = False
    return _res("V-C4", ok, det)


# ------------------------------------------------------------------------------------------------
# V-C5, V-C6, V-C8, V-C10
# ------------------------------------------------------------------------------------------------
def gate_c5_coverage(kept):
    n = max(1, len(kept))
    fb = sum(1 for v in kept if v.get("fallback_spans")) / n
    return _res("V-C5", fb <= FALLBACK_SPAN_CAP, {"fallback_share": fb, "cap": FALLBACK_SPAN_CAP, "note": "each fallback row is checked by both checkers"})


def gate_c6_drift(pool, kept):
    ok, det = PL.label_drift(pool, kept)
    return _res("V-C6", ok, {"max_abs_diff_pp": max([abs(x) for d in det.values() for x in d.values()] or [0.0]), "by_family": det})


def gate_c8_sizes(kept, n_new_rows, twin_ids, human_label_sources=frozenset(), a_rows_voice=None):
    rep = PL.shares_report(kept)
    shares_ok, det = PL.shares_within_tolerance(rep)
    per_src = collections.Counter(v["source_row_id"] for v in kept)
    voice_a = collections.Counter(v["voice"] for v in kept if v["generator"] == "A" and v.get("voice"))
    n_a = max(1, sum(voice_a.values()))
    checks = {
        "voice_share_of_new_rows": PL.voice_share_ok(len(kept), n_new_rows),
        "max_2_variants_per_source": max(per_src.values() or [0]) <= MAX_VARIANTS_PER_SOURCE,
        "clean_twin_100pct": all(v["source_row_id"] in twin_ids for v in kept),
        "zero_human_label_sources": not any(v["source_row_id"] in human_label_sources for v in kept),
        "no_voice_above_10pct_of_A": max(voice_a.values() or [0]) / n_a <= 0.10 + 1e-9,
        "shares_in_tolerance": shares_ok,
        "chunk_mode_locked": all(v.get("chunk_mode", "LOCKED-560-FLUSH") == "LOCKED-560-FLUSH" for v in kept),
    }
    return _res("V-C8", all(checks.values()), {"checks": checks, "share_detail": det, "report": rep})


def gate_c10_length(docs):
    bad = [i for i, d in enumerate(docs) if not (MIN_VERB_TOKENS <= len(d["tokens"]) <= MAX_VERB_TOKENS)]
    return _res("V-C10", not bad, {"n": len(docs), "outside": len(bad), "ids": bad[:10]})


# ------------------------------------------------------------------------------------------------
# V-C7 surface probes
# ------------------------------------------------------------------------------------------------
def surface_features(v):
    """Transcript surface only: case, punctuation, filler count, number form, length, band, generator, voice id."""
    t = v["raw_asr_text"]
    toks = t.split()
    first_up = int(bool(t) and t[0].isupper())
    n_digit_tok = sum(1 for x in toks if any(ch.isdigit() for ch in x))
    n_num_words = sum(1 for x in toks if x.lower() in W._NUMISH)
    text = "CASE_%d END_%s FILL_%d NF_%s LEN_%d BAND_%s GEN_%s VOICE_%s" % (
        first_up, "p" if t.rstrip().endswith((".", "?", "!")) else "n", sum(1 for x in toks if x.lower() in ("um", "uh", "er")),
        "d" if n_digit_tok > n_num_words else "w", len(toks) // 5, v.get("band"), v["generator"], v.get("voice"))
    num = [len(toks), len(t), n_digit_tok, n_num_words, t.count(","), t.count("."), sum(1 for ch in t if ch.isupper())]
    return text, num


def gate_c7_surface(kept, n_boot=2000, seed=0, check_sanity=True, min_rows=60):
    import probes as PB
    det, ok = {}, True
    for fam in sorted({v["source_family"] for v in kept}):
        rows = [v for v in kept if v["source_family"] == fam]
        if len(rows) < min_rows:
            det[fam] = "skipped: fewer than %d rows" % min_rows
            continue
        labels = collections.Counter(v["source_label"] for v in rows)
        majority = labels.most_common(1)[0][0]
        y = np.array([int(v["source_label"] == majority) for v in rows])
        if len(set(y.tolist())) < 2:
            det[fam] = "skipped: one class"
            continue
        feats = [surface_features(v) for v in rows]
        texts = [f[0] for f in feats]
        X = np.array([f[1] for f in feats], dtype=float)
        groups = np.array([v["source_row_id"] for v in rows])
        res = PB.run_probe("V-C7/" + fam, texts, X, y, groups, "binary", [0, 1], k=2, n_boot=n_boot or 2000, seed=seed, check_sanity=check_sanity)
        det[fam] = res
        ok &= res["status"] == "PASS"
    return _res("V-C7", ok, det)


# ------------------------------------------------------------------------------------------------
# V-C9 noiser calibration on text
# ------------------------------------------------------------------------------------------------
def gate_c9_noiser(wers, min_n=1000):
    """wers: per-variant WER measured by an INDEPENDENT implementation (solver B's own edit distance)."""
    n = len(wers)
    cnt = collections.Counter(W.band_of(w) for w in wers)
    shares = [cnt[b] / max(1, n) for b in range(4)]
    over = cnt[None] / max(1, n)
    ok = n >= min_n and all(abs(s - t) <= BAND_TOL for s, t in zip(shares, BAND_SHARE)) and over <= BAND_TOL
    return _res("V-C9", ok, {"n": n, "band_share": shares, "target": list(BAND_SHARE), "over_25pct_share": over})


def export_hashes(extra_tables=None, lexicon=None, root=None):
    root = root or os.path.dirname(os.path.abspath(__file__))
    files = ["vcommon.py", "numwords.py", "verbalizer.py", "disfluency.py", "wer.py", "span_check.py", "noiser.py", "pool.py", "planted.py", "vgates.py"]
    import hashlib
    out = {"code": {f: hashlib.sha256(open(os.path.join(root, f), "rb").read()).hexdigest() for f in files}}
    out["code_sha"] = hashlib.sha256("".join(out["code"][f] for f in files).encode()).hexdigest()
    out["tables"] = table_hashes(extra_tables)
    if lexicon is not None:
        out["lexicon"] = {"name": lexicon.name, "sha": lexicon.sha(), "n": len(lexicon.words)}
    return out
