"""Generator B: program confusion-table noiser (no model writes any text). Solver A side.

A table (harvested later from the pinned ASR on LibriSpeech TRAIN splits plus generator-A output; `harvest_table` is the CPU
function that turns (reference, hypothesis) word alignments into the table) plus fixed rules corrupts the SPOKEN-WORD tokens of a
SpokenDoc and writes an ASR-style hypothesis string. The per-token corruption probability is CALIBRATED to the WER band targets
(never a flat 10-20 percent). Decision-bearing span tokens receive no error operator; only survival-preserving FORM changes
(digits for number words, symbols for symbol words, merged letter runs) touch them, and the span checker runs afterwards on every
variant (drop-only).
"""
import copy

import numwords as NW
import span_check as SC
import wer as W
from vcommon import BAND_SHARE, FILLERS, LETTER_WORDS, NAME_TO_LETTER, SYMBOL_WORDS, VoiceError, canon_json, sha256_text

CLOSED_CLASS = frozenset("the a an of to in on at for and or but is are was were be it this that these those with from by as if so than then "
                         "do does did can could would should will shall may might must i you he she we they my your our their his her its me us them".split())
BAND_TARGET_WER = (0.015, 0.055, 0.115, 0.20)       # band centres used as calibration targets
OPS = ("drop_function_word", "double_word", "table_sub", "homophone", "split_word")

TEST_HOMOPHONES = {"two": ["to", "too"], "to": ["two"], "for": ["four"], "four": ["for"], "no": ["know"], "know": ["no"], "write": ["right"],
                   "right": ["write"], "there": ["their"], "their": ["there"], "by": ["buy"], "one": ["won"], "ate": ["eight"], "see": ["sea"]}


class ConfusionTable:
    """obj = {'version', 'key_source': 'identity'|'misaki'|'cmudict', 'subs': {key: [[word, count], ...]}, 'dels': {word: count},
    'ins': {word: count}, 'homophones': {word: [alt, ...]}, 'n_ref': int, 'source': str}"""

    def __init__(self, obj):
        for k in ("subs", "dels", "ins", "homophones", "key_source"):
            if k not in obj:
                raise VoiceError("confusion table lacks %r" % k)
        self.obj = obj

    def sha(self):
        return sha256_text(canon_json(self.obj))

    def is_production(self):
        """True only for a table harvested from named LibriSpeech TRAIN splits."""
        try:
            check_harvest_splits(self.obj.get("splits"))
        except VoiceError:
            return False
        return self.obj.get("source") not in ("TEST-ONLY", "unspecified")

    def key(self, word, g2p=None):
        if self.obj["key_source"] == "identity" or g2p is None:
            return word
        k = g2p(word)
        return k if k else word

    def sub_candidates(self, word, g2p=None):
        return self.obj["subs"].get(self.key(word, g2p), [])


TRAIN_ONLY_SPLITS = ("train-clean-100", "train-clean-360", "train-other-500")       # LibriSpeech TRAIN splits only (G0-lite section 6); never dev / test


def check_harvest_splits(splits):
    """The harvest corpus must be named and must be LibriSpeech TRAIN splits only: dev-clean, dev-other, test-clean, test-other (or anything else) refuse."""
    if not splits:
        raise VoiceError("a harvested confusion table must name its LibriSpeech splits")
    bad = [x for x in splits if x not in TRAIN_ONLY_SPLITS]
    if bad:
        raise VoiceError("splits %r are not LibriSpeech TRAIN splits: refused (no dev / test audio is ever a data source)" % (bad,))
    return tuple(splits)


def harvest_table(alignments, g2p=None, key_source="identity", source="unspecified", homophones=None, splits=None):
    """alignments: iterable of (ref_tokens, hyp_tokens) already normalised. Returns a table object (dict).
    The caller supplies the real alignments (Nemotron on LibriSpeech train splits); nothing is read from disk here.
    splits: the LibriSpeech splits the alignments come from, checked by check_harvest_splits. None is allowed only for a TEST-ONLY table
    (source == "TEST-ONLY" or "unspecified"), which a production pool refuses (`table_is_production`)."""
    if splits is not None:
        check_harvest_splits(splits)
    elif source not in ("TEST-ONLY", "unspecified"):
        raise VoiceError("a table from %r must name its LibriSpeech splits" % (source,))
    subs, dels, ins = {}, {}, {}
    n_ref = 0
    for ref, hyp in alignments:
        pairs = W.align(ref, hyp)
        n_ref += len(ref)
        for i, j in pairs:
            if i is not None and j is not None and ref[i] != hyp[j]:
                key = ref[i] if (key_source == "identity" or g2p is None) else (g2p(ref[i]) or ref[i])
                d = subs.setdefault(key, {})
                d[hyp[j]] = d.get(hyp[j], 0) + 1
            elif i is not None and j is None:
                dels[ref[i]] = dels.get(ref[i], 0) + 1
            elif i is None and j is not None:
                ins[hyp[j]] = ins.get(hyp[j], 0) + 1
    return {"version": 1, "key_source": key_source, "source": source, "splits": list(splits or []), "n_ref": n_ref, "homophones": homophones or {},
            "subs": {k: sorted([[w, c] for w, c in v.items()], key=lambda x: (-x[1], x[0])) for k, v in sorted(subs.items())},
            "dels": dict(sorted(dels.items())), "ins": dict(sorted(ins.items()))}


def _weight(tok):
    if tok in CLOSED_CLASS:
        return 2.0
    return 1.0


def noise_doc(doc, p, table, rng, g2p=None, digit_prob=0.85, symbol_prob=0.5, merge_prob=0.4):
    """Returns (hyp_text, ops). p = per-token corruption probability for ELIGIBLE tokens (before the class weights)."""
    toks = doc["tokens"]
    prot = set()
    for sp in doc["spans"]:
        prot |= set(range(sp["tok"][0], sp["tok"][1]))
    seg_of = {}
    for s in doc["segments"]:
        for t in range(s["tok"][0], s["tok"][1]):
            seg_of[t] = s
    out, ops = [], []
    i, n = 0, len(toks)
    while i < n:
        seg = seg_of.get(i)
        kind = seg["kind"] if seg else "word"
        a, b = (seg["tok"] if seg else (i, i + 1))
        words = toks[a:b]
        if seg["src"] is not None and seg["kind"] in ("spelled", "digits", "sym") and _is_code_unit(doc, seg):
            # a code-like source token: the ASR either writes it as one written identifier or as separate letters / symbols
            ua, ub = _unit_range(doc, seg)
            if seg["tok"][0] != ua:
                i = b
                continue
            if rng.random() < merge_prob:
                out.append(doc["source_tokens"][seg["src"]].lower())
                ops.append(("write_identifier", ua))
                i = ub
                continue
            for s2 in [s for s in doc["segments"] if s["src"] == seg["src"]]:
                w2 = toks[s2["tok"][0]:s2["tok"][1]]
                if s2["kind"] == "spelled":
                    out += [NAME_TO_LETTER.get(x, x) for x in w2 if x != "capital"]
                elif s2["kind"] == "sym" and s2.get("char") and rng.random() < symbol_prob:
                    out.append(s2["char"])
                elif s2["kind"] == "digits":
                    out.append("".join(NW.WORD_DIGIT.get(x, x) for x in w2))
                else:
                    out += w2
            i = ub
            continue
        elif kind == "spelled":
            out += [NAME_TO_LETTER.get(w, w) for w in words if w != "capital"]
        elif kind in ("number", "digits") and len(words) >= 1:
            if rng.random() < digit_prob:
                cands = _number_digits(words)
                if cands:
                    out.append(cands)
                    ops.append(("number_to_digits", a))
                else:
                    out += words
            else:
                out += words
        elif kind == "sym":
            ch = seg.get("char")
            if ch and rng.random() < symbol_prob:
                out.append(ch)
                ops.append(("symbol_char", a))
            else:
                out += words
        elif kind == "disfl":
            out += words
        else:
            # plain words (and word/hyphen segments): error operators only outside decision spans
            for k, w in enumerate(words):
                idx = a + k
                if idx in prot or rng.random() >= p * _weight(w):
                    out.append(w)
                    continue
                choices = []
                if w in CLOSED_CLASS:
                    choices.append("drop_function_word")
                choices.append("double_word")
                if table.sub_candidates(w, g2p):
                    choices.append("table_sub")
                if w in table.obj["homophones"]:
                    choices.append("homophone")
                if len(w) >= 6:
                    choices.append("split_word")
                op = rng.choice(choices)
                if op == "drop_function_word":
                    ops.append((op, idx))
                elif op == "double_word":
                    out += [w, w]
                    ops.append((op, idx))
                elif op == "table_sub":
                    cands = table.sub_candidates(w, g2p)
                    tot = sum(c for _, c in cands)
                    r = rng.random() * tot
                    acc = 0
                    for to, c in cands:
                        acc += c
                        if r <= acc:
                            out.append(to)
                            break
                    ops.append((op, idx))
                elif op == "homophone":
                    out.append(rng.choice(table.obj["homophones"][w]))
                    ops.append((op, idx))
                else:
                    cut = rng.randint(2, len(w) - 2)
                    out += [w[:cut], w[cut:]]
                    ops.append((op, idx))
        i = b
    return " ".join(out), ops


def _unit_segments(doc, seg):
    return sorted([s for s in doc["segments"] if s["src"] == seg["src"]], key=lambda s: s["tok"][0])


def _is_code_unit(doc, seg):
    return len(_unit_segments(doc, seg)) >= 2 or seg["kind"] in ("spelled", "sym")


def _unit_range(doc, seg):
    ss = _unit_segments(doc, seg)
    return ss[0]["tok"][0], ss[-1]["tok"][1]


def _number_digits(words):
    import numwords as NW
    c = NW.parse_number_tokens([w for w in words])
    if not c:
        return None
    return sorted(c, key=lambda x: (len(x), x))[0] if len(c) == 1 else None


def calibrate(docs, target_wer, table, seed_rng_fn, iters=14, hi=0.9, **kw):
    """Bisection on p so the mean measured WER over `docs` hits `target_wer`. seed_rng_fn(k) -> a fresh random.Random for pass k."""
    lo_p, hi_p = 0.0, hi
    best = (0.0, 1e9)
    for it in range(iters):
        mid = (lo_p + hi_p) / 2
        tot = 0.0
        for k, d in enumerate(docs):
            h, _ = noise_doc(d, mid, table, seed_rng_fn(1000 * it + k), **kw)
            tot += SC.doc_wer(d, h)[0]
        m = tot / max(1, len(docs))
        if abs(m - target_wer) < best[1]:
            best = (mid, abs(m - target_wer))
        if m < target_wer:
            lo_p = mid
        else:
            hi_p = mid
    return best[0]
